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


@router.get('/', name='wine')
async def wine_list(request: Request):
    # await request.app.mongo['wine'].clear_db()
    return templates.TemplateResponse("wine/wine.html", {"request": request})


@router.post('/get_wine', name='get_wine')
async def get_wine(request: Request, data: Dict[str, Any]):
    wine, pagination = await get_items(request, 'wine', data['page'], data['sorting'])
    return {'wine': wine, 'pagination': pagination}


@router.get('/add_wine', name='add_wine')
async def add_wine_template(request: Request):
    return templates.TemplateResponse("wine/add_wine.html", {"request": request})


@router.post('/get_wine_item', name='get_wine_item')
async def get_wine_item(request: Request, data: Dict[str, Any]):
    wine = await get_item(request, 'wine', data['id'])
    return {'wine': wine}


# TODO распилить нормально
@router.post('/api/add_wine', name='add_wine', tags=['protected'])
async def add_wine(
    request: Request,
    *,
    name: str = Form(...),
    rate: int = Form(...),
    review: str = Form(''),
    others: str = Form(''),
    manufacturer: str = Form(''),
    photos: List[UploadFile] = [],
    alcohol: float = Form(''),
    style: str = Form(''),
    sugar: str = Form(''),
):
    data = {
        'name': name,
        'rate': rate,
        'review': review,
        'others': others,
        'photos': photos,
        'sugar': sugar,
        'style': style,
        'alcohol': alcohol,
        'manufacturer': manufacturer,
    }
    return await save_item_to_base(request, data, 'wine')
