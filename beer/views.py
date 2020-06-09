from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common.utils import get_items, get_item, save_item_to_base
from beer.scheme import AddBeer, BeerList, BeerItem

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
    return templates.TemplateResponse("beer/beer.html", {"request": request})


@router.get('/add_beer', name='add_beer')
async def add_beer_template(request: Request):
    return templates.TemplateResponse("beer/add_beer.html", {"request": request})


@router.post('/get_beer', name='get_beer')
async def get_beer(request: Request, settings: BeerList):
    page, sorting, query = settings.page, settings.sorting, settings.query
    beer, pagination = await get_items(request, 'beer', page, sorting, query)
    return {'beer': beer, 'pagination': pagination}


@router.post('/get_beer_item', name='get_beer_item')
async def get_beer_item(request: Request, beer_data: BeerItem):
    beer = await get_item(request, 'beer', beer_data.id)
    return {'beer': beer}


@router.post('/api/add_beer', name='add_beer', tags=['protected'])
async def add_beer(
    request: Request,
    item: AddBeer = Depends(AddBeer.as_form)
):
    return await save_item_to_base(request, item.dict(), 'beer')
