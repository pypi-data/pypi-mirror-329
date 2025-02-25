from urllib.parse import urlparse

from fastapi.responses import HTMLResponse

html = "<!doctype html><title>FastAPI OIDC</title><style>body{background-color:#f4f4f4;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.container{text-align:center;background:#fff;padding:40px;border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,.1);max-width:500px;width:90%}h1{color:#444}.login-links p{margin:10px 0}.login-links a{text-decoration:none;background:#333;color:#fff;padding:10px 20px;border-radius:5px;display:inline-block}.login-links a:hover{background:#555}.user-info{margin-top:20px}.user-info p{margin:5px 0;font-size:20px}.user-info img{margin-top:10px;border-radius:50%;border:2px solid #ddd}button{background:#d9534f;color:#fff;border:none;padding:10px 20px;font-size:20px;border-radius:5px;cursor:pointer;margin-top:15px}button:hover{background:#c9302c}</style><div class=container><h1>FastAPI OIDC</h1>" # noqa
login_item = '<p><img style="margin-bottom: -10px;margin-right: 10px" width="30" height="30" src="{logo}"/><a href="{url}">Login with <strong>{name}</strong></a></p>' # noqa
user_info = "<div class=user-info><h3 style=color:green>Login Succeeded</h3><p>Signed in as <strong>{name}</strong> (id: <span>{sub}</span>)</p><small>{email}</small><br><img height=100 src={picture} width=100><form action={logout_url} method=POST><button type=submit>Logout</button></form></div>"  # noqa


def get_logo_url(provider_url):
    parsed_url = urlparse(provider_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url + '/favicon.ico'


def test_page(providers, user, logout_url):
    if not user:
        content = '<div class="login-links">' + ''.join(
            login_item.format(
                url=provider.url,
                name=provider.name,
                logo=get_logo_url(provider.provider_url)
            )
            for provider in providers
        ) + '</div>'
    else:
        content = user_info.format(**user.model_dump(), logout_url=logout_url)

    return HTMLResponse(html + content + '</div></body></html>')
