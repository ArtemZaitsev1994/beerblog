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


@router.get('/', name='beer')
async def beer_list(request: Request, page: int = 1):
    # await request.app.mongo['beer'].clear_db()
    beer, pagination = await request.app.mongo['beer'].get_all()
    print(beer)
    return templates.TemplateResponse("beer.html", {"request": request, 'beer': beer, 'pagination': pagination})


@router.get('/add_beer', name='add_beer')
async def add_beer_template(request: Request):
    return templates.TemplateResponse("add_beer.html", {"request": request})


class BeerDataIn(BaseModel):
    name: str = Form(...)
    rate: int = Form(...)
    manufacturer: str = Form(...)
    fortress: int = Form(...)
    gravity: int = Form(...)
    review: str = Form(...)
    others: str = Form(...)
    photo: List[UploadFile] = File(...)


@router.post('/add_beer', name='add_beer', response_model=CommonResponse)
async def add_beer(
    request: Request,
    *,
    name: str = Form(...),
    rate: int = Form(...),
    manufacturer: str = Form(...),
    fortress: int = Form(...),
    gravity: int = Form(...),
    review: str = Form(...),
    others: str = Form(...),
    photos: List[UploadFile] = File(...)
):
    data = {
        'name': name,
        'rate': rate,
        'manufacturer': manufacturer,
        'fortress': fortress,
        'gravity': gravity,
        'review': review,
        'others': others,
    }

    photo_dir = request.app.beer_photo_path
    filenames = []
    for photo in photos:
        filename = uuid4().hex
        async with AIOFile(os.path.join(photo_dir, filename), 'wb') as f:
            await f.write(await photo.read())
        filenames.append(filename)

    data['photos'] = {
        'filenames': filenames,
    }
    result = await request.app.mongo['beer'].insert_item(data)

    if result.acknowledged:
        return {'acknowledged': True}
    else:
        return {'acknowledged': False, 'message': 'Insert failed', 'error_data': data}


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
