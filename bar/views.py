from typing import Dict, Any, List

from fastapi import APIRouter, Request, Form, UploadFile
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common.utils import get_items, get_item, save_item_to_base


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


@router.post('/get_bar', name='get_bar')
async def get_bar(request: Request, data: Dict[str, Any]):
    bar, pagination = await get_items(request, 'bar', data['page'], data['sorting'], data.get('query', ''))
    return {'bar': bar, 'pagination': pagination}


@router.get('/add_bar', name='add_bar')
async def add_bar_template(request: Request):
    return templates.TemplateResponse("bar/add_bar.html", {"request": request})


@router.post('/get_bar_item', name='get_bar_item')
async def get_bar_item(request: Request, data: Dict[str, Any]):
    bar = await get_item(request, 'bar', data['id'])
    return {'bar': bar}


@router.post('/api/add_bar', name='add_bar', tags=['protected'])
async def add_bar(
    request: Request,
    *,
    name: str = Form(...),
    rate: int = Form(...),
    review: str = Form(''),
    others: str = Form(''),
    address: str = Form(''),
    worktime: str = Form(''),
    city: str = Form(''),
    country: str = Form(''),
    site: str = Form(''),
    photos: List[UploadFile] = [],
):
    data = {
        'name': name,
        'rate': rate,
        'review': review,
        'others': others,
        'photos': photos,
        'address': address,
        'worktime': worktime,
        'city': city,
        'site': site,
        'country': country,
    }
    return await save_item_to_base(request, data, 'bar')
