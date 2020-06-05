from typing import Dict, Any

import jwt
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

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


# # TODO распилить нормально
# @router.post('/api/save_item', name='save_item', tags=['protected'])
# async def save_item(
#     request: Request,
#     *,
#     name: str = Form(...),
#     rate: int = Form(...),
#     review: str = Form(''),
#     others: str = Form(''),

#     manufacturer: str = Form(''),
#     photos: List[UploadFile] = [],
#     alcohol: float = Form(''),

#     ibu: int = Form(''),
#     fortress: float = Form(''),

#     style: str = Form(''),
#     sugar: str = Form(''),

#     address: str = Form(''),
#     worktime: str = Form(''),
#     city: str = Form(''),
#     country: str = Form(''),

#     item_type: str = Form(...),
# ):
#     data = {
#         'name': name,
#         'rate': rate,
#         'review': review,
#         'others': others,
#         'photos': photos,
#     }

#     if item_type == 'wine':
#         data.update({
#             'sugar': sugar,
#             'style': style,
#             'alcohol': alcohol,
#             'manufacturer': manufacturer,
#         })
#     elif item_type == 'beer':
#         data.update({
#             'fortress': fortress,
#             'ibu': ibu,
#             'alcohol': alcohol,
#             'manufacturer': manufacturer,
#         })
#     elif item_type == 'bar':
#         data.update({
#             'address': address,
#             'worktime': worktime,
#             'city': city,
#             'country': country,
#         })
#     return await save_item_to_base(request, data, item_type)


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
