import os
from typing import Dict, Any

import jwt
from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from aiofile import AIOFile
from uuid import uuid4
from typing import List
from PIL import Image

from settings import AUTH_SERVER_LINK, JWT_ALGORITHM, JWT_SECRET_KEY


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


@router.post('/api/save_item', name='save_item', tags=['protected'])
async def save_item(
    request: Request,
    *,
    name: str = Form(...),
    rate: int = Form(...),
    manufacturer: str = Form(''),
    alcohol: float = Form(''),
    fortress: float = Form(''),
    style: str = Form(''),
    sugar: str = Form(''),
    ibu: int = Form(''),
    review: str = Form(''),
    others: str = Form(''),
    photos: List[UploadFile] = [],
    alcohol_type: str = Form(...)
):
    data = {
        'name': name,
        'rate': rate,
        'manufacturer': manufacturer,
        'review': review,
        'others': others,
    }

    if alcohol_type == 'wine':
        data.update({
            'sugar': sugar,
            'style': style,
            'alcohol': alcohol,
        })
    elif alcohol_type == 'beer':
        data.update({
            'fortress': fortress,
            'ibu': ibu,
            'alcohol': alcohol,
        })
    photo_dir = request.app.photo_path[alcohol_type]

    # велосипед
    token = request.headers['Authorization']
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    data['author'] = payload['login']

    filenames = []
    for photo in photos:
        if photo.filename == '':
            break
        filename = uuid4().hex
        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir)
        image_path = os.path.join(photo_dir, filename)
        async with AIOFile(image_path, 'wb') as f:
            await f.write(await photo.read())
        filenames.append(filename)

    avatar_name = ''
    if len(filenames) > 0:
        avatar_dir = os.path.join(photo_dir, "avatars/")
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)
        avatar = Image.open(image_path)
        buff_size = avatar.size[0] // 40
        h, w = int(avatar.size[0] / buff_size), int(avatar.size[1] / buff_size)
        avatar = avatar.resize((h, w), Image.ANTIALIAS)
        avatar_path = os.path.join(avatar_dir, f'avatar_{filename}.png')
        avatar = avatar.save(avatar_path, quality=30)
        avatar_name = f'avatar_{filenames[0]}.png'

    data['photos'] = {
        'filenames': filenames,
        'avatar': avatar_name
    }
    result = await request.app.mongo[alcohol_type].insert_item(data)

    if result.acknowledged:
        response = {'success': True}
    else:
        response = {
            'success': False,
            'message': 'Insert failed at the serverside. Call Тёма, scream and run around',
            'error_data': data
        }
    return response


@router.post('/api/check_token', name='check_token', tags=['trusted'])
async def check_token(request: Request):
    """Заглушка для проверки токена, токен проверится в миддлвари"""
    return {'success': True}


@router.post('/get_auth_link', name='get_auth_link')
async def get_auth_link(request: Request, data: Dict[str, str]):
    section = data.get('section')
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
async def add_comment(request: Request, data: Dict[str, Any]):
    response = {
        'success': False
    }

    alcohol_type = data.get('alcohol_type')
    result = await request.app.mongo[alcohol_type].add_comment(data['_id'], data['comment'])

    if result.acknowledged:
        response['success'] = True
    return response


@router.post('/api/update_rate', name='update_rate')
async def update_rate(request: Request, data: Dict[str, Any]):
    response = {
        'success': False
    }

    alcohol_type = data.get('alcohol_type')
    result, new_rate = await request.app.mongo[alcohol_type].update_rate(data['_id'], data['rate'], data['login'])

    if result.acknowledged:
        response['success'] = True
        response['newRate'] = new_rate

    return response
