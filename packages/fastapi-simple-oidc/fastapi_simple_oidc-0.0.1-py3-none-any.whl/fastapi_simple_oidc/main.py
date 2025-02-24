"""OIDC module"""
from typing import Callable
from urllib.parse import urljoin

import httpx
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from fastapi_simple_oidc.quick_test import test_page
from fastapi_simple_oidc.settings import SSOConfig, Settings

DEFAULT_PROVIDERS = {
    "Google": "https://accounts.google.com",
    "Microsoft": "https://login.microsoftonline.com/{tenant}/v2.0",
    "Apple": "https://appleid.apple.com",
    "GitLab": "https://gitlab.com",
    "Salesforce": "https://login.salesforce.com",
    "IBM": "https://iam.cloud.ibm.com/identity"
}
DEFAULT_PROVIDERS_BY_NAME = {
    k.upper(): v for k, v in DEFAULT_PROVIDERS.items()
}
PROVIDERS_DISPLAY_NAMES = {k.upper(): k for k in DEFAULT_PROVIDERS}


class DiscoveryDocument(BaseModel):
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    display_name: str | None = None


class OpenID(BaseModel):
    sub: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    provider: str | None = None


class SSOProvider(BaseModel):
    name: str
    display_name: str
    provider_url: str
    url: str


oauth = OAuth()


class OIDC:
    def __init__(self, app, secret_key, login_url: str = '/login', redirect_url: str = '/'):
        """Initializes the OIDC authentication handler for a FastAPI application.

        This constructor sets up authentication using OpenID Connect (OIDC) with
        cookie-based session management.

        Args:
            app: The FastAPI application instance.
            secret_key (str): A secret key used for securing cookie-based sessions.
            login_url (str, optional): The URL to redirect users to when they log out.
                                       Defaults to '/login'.
            redirect_url (str, optional): The URL to redirect users to after a
                                          successful login. Defaults to '/'.
        """
        app.add_middleware(
            SessionMiddleware,
            secret_key=secret_key,
            session_cookie="sso_session"
        )
        self.providers = {}
        self.login_home_url = login_url
        self.redirect_url = redirect_url

        self._configure_providers()
        self.router = self._configure_router()

        self._on_login: Callable | None = None
        self._on_logout: Callable | None = None

    def on_login(self, f):
        """On login event decorator"""
        self._on_login = f

    def on_logout(self, f):
        """On logout event decorator"""
        self._on_logout = f

    def _configure_providers(self):
        load_dotenv()
        settings = Settings()

        for provider_name, sso_config in settings.sso.items():
            discovery = self._configure_provider(provider_name, sso_config)
            discovery.display_name = sso_config.name or provider_name
            self.providers[provider_name] = discovery

    def _configure_router(self) -> APIRouter:
        api_router = APIRouter()
        for prodiver in self.providers:
            router = self._get_provider_router(prodiver)
            api_router.include_router(router, prefix=f"/{prodiver}")

        @api_router.post("/logout")
        async def logout(request: Request):
            """Logout user by clearing the session"""
            user = request.session.pop("user", None)
            if self._on_logout and user:
                self._on_logout(OpenID(**user))

            return RedirectResponse(url=self.login_home_url)

        @api_router.get("/providers")
        async def providers(req: Request):
            """Logout user by clearing the session"""
            return self._get_providers(req)

        @api_router.get("/me")
        async def me(user=Depends(get_logged_user)):
            """Logout user by clearing the session"""
            return user

        @api_router.get("/.test", include_in_schema=False)
        async def test(req: Request):
            try:
                user = await get_logged_user(req)
            except Exception:
                user = None
            logout_url = str(req.url).split('/.test')[0] + '/logout'
            return test_page(self._get_providers(req), user, logout_url)

        return api_router

    def _get_providers(self, req: Request):
        return [
            SSOProvider(
                name=provider,
                display_name=discovery.display_name or provider,
                url=str(req.url).rsplit('/', 1)[0] + f'/{provider}/login',
                provider_url=discovery.authorization_endpoint,
            )
            for provider, discovery in self.providers.items()
        ]

    def _configure_provider(
        self, name: str, sso_config: SSOConfig
    ) -> DiscoveryDocument:
        if not sso_config.url:
            if name not in DEFAULT_PROVIDERS_BY_NAME:
                raise ValueError(
                    f"Provider {name} doesn't have a default auth URL, "
                    f"provide it with SSO_<PROVIDER>_URL"
                )
            sso_config.url = DEFAULT_PROVIDERS_BY_NAME[sso_config.name]

        if not sso_config.name:
            sso_config.name = PROVIDERS_DISPLAY_NAMES.get(
                sso_config.name, name.capitalize()
            )

        discovery = get_openid_discovery(sso_config.url)

        oauth.register(
            name=name,
            client_id=sso_config.id,
            client_secret=sso_config.secret,
            authorize_url=discovery.authorization_endpoint,
            authorize_params=None,
            access_token_url=discovery.token_endpoint,
            access_token_params=None,
            client_kwargs={"scope": "openid email profile"},
            server_metadata_url=urljoin(
                sso_config.url, '/.well-known/openid-configuration'
            )
        )

        return discovery

    def _get_provider_router(self, provider) -> APIRouter:
        router = APIRouter(tags=['sso'])
        discovery = self.providers[provider]

        @router.get("/login")
        async def login(request: Request):
            """Redirect user to the authorization URL of the ID Provider"""
            base_url = str(request.url).split(f"{provider}/")[0]
            return await getattr(oauth, provider).authorize_redirect(
                request, base_url + f'{provider}/callback'
            )

        @router.get("/callback")
        async def callback(request: Request):
            """Handle callback from the identity provider"""

            token = await getattr(
                oauth, provider
            ).authorize_access_token(request)

            user = await getattr(
                oauth, provider
            ).get(
                discovery.userinfo_endpoint, token=token
            )
            user = user.json()
            request.session["user"] = user

            if self._on_login:
                self._on_login(OpenID(**user))

            return RedirectResponse(url=self.redirect_url)

        return router


def get_openid_discovery(sso_url: str) -> DiscoveryDocument:
    res = httpx.get(urljoin(sso_url, '/.well-known/openid-configuration'))
    return DiscoveryDocument(**res.json())


async def get_logged_user(request: Request) -> OpenID:
    """Get current logged user.
    If user is not logged in - raise HTTPException
    """
    if not (user := request.session.get("user")):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return OpenID(**user)
