from os import access
from fastapi import responses
import requests
from typing import Optional

from fastapi import FastAPI, Depends, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from pydantic import BaseSettings


class Settings(BaseSettings):
    oauth_host: str = 'http://127.0.0.1:8998'
    oauth_client_id: str
    oauth_client_secret: str

    class Config:
        env_file = '.env'


settings = Settings()

sessions_db = {}

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


async def get_current_user():
    token = sessions_db.get('dima')
    exc = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='Not authenticated',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    if not token:
        raise exc

    response = requests.get(
        f'{settings.oauth_host}/users/me/',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    if response.status_code != 200:
        raise exc

    user = response.json()
    return {'user': user}


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'sign_in_url': f'{settings.oauth_host}/o/authorize/?response_type=code&client_id=U0TsRB8vhpoyeAlDineMpHwxOnK1EhpalgnHGFQT&state=random_state_string',
        },
    )


@app.get('/me')
async def me(user: dict = Depends(get_current_user)):
    return user


@app.get('/auth/callback')
async def auth_callback(code: str):
    oauth2_response = requests.post(
        f'{settings.oauth_host}/o/token/',
        data={
            'client_id': settings.oauth_client_id,
            'client_secret': settings.oauth_client_secret,
            'code': code,
            'grant_type': 'authorization_code',
        },
    )
    data = oauth2_response.json()
    access_token = data['access_token']

    sessions_db['dima'] = access_token

    return access_token
