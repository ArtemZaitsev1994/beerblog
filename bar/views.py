from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common.utils import get_items, get_item, save_item_to_base
from bar.scheme import AddBar, BarList, BarItem


templates = Jinja2Templates(directory="templates")
router = APIRouter()


class CommonResponse(BaseModel):
    acknowledged: bool
    message: str = None
    error_data: str = None


@router.get('/', name='bar')
async def bar_list(request: Request):
    # await request.app.mongo['wine'].clear_db()
    return templates.TemplateResponse("bar/bar.html", {"request": request})


@router.get('/add_bar', name='add_bar')
async def add_bar_template(request: Request):
    return templates.TemplateResponse("bar/add_bar.html", {"request": request})


@router.post('/get_bar', name='get_bar')
async def get_bar(request: Request, settings: BarList):
    page, sorting, query = settings.page, settings.sorting, settings.query
    bar, pagination = await get_items(request, 'bar', page, sorting, query)
    return {'bar': bar, 'pagination': pagination}


@router.post('/get_bar_item', name='get_bar_item')
async def get_bar_item(request: Request, bar_data: BarItem):
    bar = await get_item(request, 'bar', bar_data.id)
    return {'bar': bar}


@router.post('/api/add_bar', name='add_bar', tags=['protected'])
async def add_bar(
    request: Request,
    item: AddBar = Depends(AddBar.as_form)
):
    return await save_item_to_base(request, item.dict(), 'bar')
