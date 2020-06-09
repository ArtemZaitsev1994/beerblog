from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common.utils import get_items, get_item, save_item_to_base
from wine.scheme import AddWine, WineList, WineItem


templates = Jinja2Templates(directory="templates")
router = APIRouter()


class CommonResponse(BaseModel):
    acknowledged: bool
    message: str = None
    error_data: str = None


@router.get('/', name='wine')
async def wine_list(request: Request):
    # await request.app.mongo['wine'].clear_db()
    return templates.TemplateResponse("wine/wine.html", {"request": request})


@router.get('/add_wine', name='add_wine')
async def add_wine_template(request: Request):
    return templates.TemplateResponse("wine/add_wine.html", {"request": request})


@router.post('/get_wine', name='get_wine')
async def get_wine(request: Request, settings: WineList):
    page, sorting, query = settings.page, settings.sorting, settings.query
    wine, pagination = await get_items(request, 'wine', page, sorting, query)
    return {'wine': wine, 'pagination': pagination}


@router.post('/get_wine_item', name='get_wine_item')
async def get_wine_item(request: Request, wine_data: WineItem):
    wine = await get_item(request, 'wine', wine_data.id)
    return {'wine': wine}


# TODO распилить нормально
@router.post('/api/add_wine', name='add_wine', tags=['protected'])
async def add_wine(
    request: Request,
    item: AddWine = Depends(AddWine.as_form)
):
    return await save_item_to_base(request, item, 'wine')
