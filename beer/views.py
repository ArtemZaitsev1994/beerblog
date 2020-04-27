import os
from uuid import uuid4
from typing import List

import graphene
from fastapi import APIRouter, Request, UploadFile, File, Form, Body
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.graphql import GraphQLApp
from aiofile import AIOFile


templates = Jinja2Templates(directory="templates")
router = APIRouter()


class CommonResponse(BaseModel):
    acknowledged: bool
    message: str = None
    error_data: str = None


@router.get('/articles', name='articles')
async def articles(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})


@router.get('/', name='beer')
async def beer_list(request: Request):
    # await request.app.mongo['beer'].clear_db()
    return templates.TemplateResponse("beer.html", {"request": request})


@router.post('/get_beer', name='get_beer')
async def get_beer(request: Request, page: int = 1, q: str = ''):
    beer, pagination = await request.app.mongo['beer'].get_all(page=page)
    for b in beer:
        b['_id'] = str(b['_id'])
        if len(b['photos']['filenames']) == 0:
            b['avatar'] = request.url_for("photo", path='./beer/beer_default.png')
        else:
            b['avatar'] = request.url_for('photo', path=f"./beer/{b['photos']['filenames'][0]}")
    pagination['prev_link'] = request.url_for('get_beer') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_beer') + f'?page={page+1}'
    return {'beer': beer, 'pagination': pagination}


@router.get('/add_beer', name='add_beer')
async def add_beer_template(request: Request):
    return templates.TemplateResponse("add_beer.html", {"request": request})


# class BeerDataIn(BaseModel):
#     name: str = Form(...)
#     rate: int = Form(...)
#     manufacturer: str = Form(...)
#     fortress: int = Form(...)
#     gravity: int = Form(...)
#     review: str = Form(...)
#     others: str = Form(...)
#     photo: List[UploadFile] = File(...)


# @router.post('/add_beer', name='add_beer', response_model=CommonResponse)
# async def add_beer(
#     request: Request,
#     *,
#     name: str = Form(...),
#     rate: int = Form(...),
#     manufacturer: str = Form(''),
#     fortress: float = Form(''),
#     gravity: int = Form(''),
#     ibu: int = Form(''),
#     review: str = Form(''),
#     others: str = Form(''),
#     photos: List[UploadFile] = File(None)
# ):
#     data = {
#         'name': name,
#         'rate': rate,
#         'manufacturer': manufacturer,
#         'fortress': fortress,
#         'gravity': gravity,
#         'review': review,
#         'others': others,
#         'ibu': ibu,
#     }

#     photo_dir = request.app.beer_photo_path
#     filenames = []
#     for photo in photos:
#         if photo.filename == '':
#             break
#         filename = uuid4().hex
#         async with AIOFile(os.path.join(photo_dir, filename), 'wb') as f:
#             await f.write(await photo.read())
#         filenames.append(filename)

#     data['photos'] = {
#         'filenames': filenames,
#     }
#     result = await request.app.mongo['beer'].insert_item(data)

#     if result.acknowledged:
#         response = {'acknowledged': True}
#     else:
#         response = {
#             'acknowledged': False,
#             'message': 'Insert failed on serverside. Call Тёма, scream and run around',
#             'error_data': data
#         }
#     return response

# class CreateBeer(graphene.Mutation):
#     class Arguments:
#         name = graphene.String()
#         rate: int
#         manufacturer = graphene.String()
#         fortress: int = None
#         gravity: int = None
#         review = graphene.String()
#         others = graphene.String()


# class Mutation(graphene.ObjectType):
#     beer = CreateBeer.Field()

#     async def resolve_addBeer(self, info, request: Request, *, data: BeerDataIn):
#         pass


# router.add_route('/beer_query', GraphQLApp(schema=graphene.Schema(mutation=Mutation)))
