from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from common.utils import get_items, get_item, save_item_to_base
from bar.scheme import AddBar, BarList, BarItem


router = APIRouter()


class CommonResponse(BaseModel):
    acknowledged: bool
    message: str = None
    error_data: str = None


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
