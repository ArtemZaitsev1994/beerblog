from typing import Dict

import jwt
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from settings import AUTH_SERVER_LINK, JWT_ALGORITHM, JWT_SECRET_KEY
from common.scheme import Comment, ItemRating


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/', name='common')
def beer_list(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/articles', name='articles')
async def articles(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})


@router.get('/contacts', name='contacts')
async def contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@router.post('/api/check_token', name='check_token', tags=['trusted'])
async def check_token(request: Request):
    """Заглушка для проверки токена, токен проверится в миддлвари"""
    return {'success': True}


@router.post('/get_auth_link', name='get_auth_link')
async def get_auth_link(request: Request, data: Dict[str, str]):
    section = data.get('section', 'beer')
    response = {
        'link': AUTH_SERVER_LINK.format(section),
        'success': True
    }
    return response


@router.get('/auth/{token}', name='auth')
async def auth(request: Request, token: str):
    urls = {
        'beer': 'add_beer',
        'wine': 'add_wine',
        'vodka': 'add_vodka'
    }
    """Метод для принятия авторизации"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return RedirectResponse(AUTH_SERVER_LINK)

    redirect_to = urls.get(payload['section'], '/')
    response = RedirectResponse(request.url_for(redirect_to))
    response.set_cookie(key='Authorization', value=token)
    return response


@router.post('/api/add_comment', name='add_comment')
async def add_comment(request: Request, comment: Comment):
    response = {
        'success': False
    }

    alcohol_type = comment.alcohol_type
    result = await request.app.mongo[alcohol_type].add_comment(comment.itemId, comment.comment)

    if result.acknowledged:
        response['success'] = True
    return response


@router.post('/api/update_rate', name='update_rate')
async def update_rate(request: Request, rating_data: ItemRating):
    response = {
        'success': False
    }

    itemId, rate, login = rating_data.itemId, rating_data.rate, rating_data.login
    alcohol_type = rating_data.alcohol_type
    result, new_rate = await request.app.mongo[alcohol_type].update_rate(itemId, rate, login)

    if result.acknowledged:
        response['success'] = True
        response['newRate'] = new_rate

    return response
