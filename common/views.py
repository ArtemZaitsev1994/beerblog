import os
import json
from typing import Dict

import jwt
from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from aiofile import AIOFile
from uuid import uuid4
from typing import List

from settings import AUTH_SERVER_LINK, JWT_ALGORITHM, JWT_SECRET_KEY, CHANGE_PASSWORD_LINK


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


@router.get('/login_page', name='login_page')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/profile', name='profile')
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.post('/api/save_item', name='save_item', tags=['protected'])
async def save_item(
    request: Request,
    data: Dict[str, str]
    # *,
    # name: str = Form(...),
    # rate: int = Form(...),
    # manufacturer: str = Form(''),
    # alcohol: float = Form(''),
    # fortress: int = Form(''),
    # style: str = Form(''),
    # sugar: str = Form(''),
    # ibu: int = Form(''),
    # review: str = Form(''),
    # others: str = Form(''),
    # photos: List[UploadFile] = [],
    # alcohol_type: str = Form(...)
):
    # data = {
    #     'name': name,
    #     'rate': rate,
    #     'manufacturer': manufacturer,
    #     'review': review,
    #     'others': others,
    #     'not_confirmed': True
    # }

    # if alcohol_type == 'wine':
    #     data.update({
    #         'sugar': sugar,
    #         'style': style,
    #         'alcohol': alcohol,
    #     })
    # elif alcohol_type == 'beer':
    #     data.update({
    #         'fortress': fortress,
    #         'ibu': ibu,
    #         'alcohol': alcohol,
    #     })

    photo_dir = request.app.photo_path[data['alcohol_type']]

    # велосипед
    token = request.headers['Authorization']
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    data['author'] = payload['login']

    # elastic_data = data.copy()

    filenames = []
    if data.get('photos'):
        for photo in data['photos']:
            filename = uuid4().hex
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir)
            async with AIOFile(os.path.join(photo_dir, filename), 'wb') as f:
                await f.write(await photo.read())
            filenames.append(filename)

    data['photos'] = {
        'filenames': filenames,
    }
    # запись в MongoDB
    result = await request.app.mongo[data['alcohol_type']].insert_item(data)

    # запись в ElasticSearch
    # elastic_data['mongo_id'] = str(result.inserted_id)
    # await request.app.es_client.index(
    #     index=alcohol_type,
    #     body=elastic_data
    # )

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


@router.post('/search', name='search')
async def search(request: Request, data: Dict[str, str]):
    # query = {
    #     "query": {
    #         "bool": {
    #             "should": [
    #                 {"term": {"review": data['query']}},
    #                 {"term": {"manufacturer": data['query']}},
    #                 {"term": {"rate": data['query']}},
    #                 {"term": {"others": data['query']}},
    #                 {"term": {"name": data['query']}}
    #             ],
    #             "minimum_should_match": 1,
    #             "boost": 1.0
    #         }
    #     }
    # }
    return {'success': True}
    query = {
        'query': {
            "match": {
                "review": data['query']
            }
        }
    }
    print(data)
    result = await request.app.es_client.search(index=data['alcohol_type'], body=query)
    print(result['hits']['hits'])
    return {'beer': [x['_source'] for x in result['hits']['hits']], 'pagination': ''}


@router.get('/auth/{token}', name='auth')
async def auth(request: Request, token: str):
    """DEPRECATED"""
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


@router.post('/login', name='login')
async def login(request: Request, data: Dict[str, str]):
    content = {
        'success': True,
    }

    async with request.app.http_client() as client:
        response = await client.post(AUTH_SERVER_LINK, data=json.dumps(data))
    response_data = json.loads(response.text)

    if response_data['success']:
        response = JSONResponse(content=content)
        response.set_cookie(key='Authorization', value=response_data['token'])
    else:
        content['message'] = response_data['message']
        content['success'] = False
        response = JSONResponse(content=content)

    return response


@router.post('/change_password', name='change_password')
async def change_password(request: Request, data: Dict[str, str]):
    content = {
        'success': True,
    }

    data['login'] = request.state.login
    async with request.app.http_client() as client:
        response = await client.post(CHANGE_PASSWORD_LINK, data=json.dumps(data))
    response_data = json.loads(response.text)
    print(response_data)

    if not response_data['success']:
        content['success'] = False
        content['message'] = response_data['message']

    response = JSONResponse(content=content)
    return response
