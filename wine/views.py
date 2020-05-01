from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from common.utils import get_items


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
async def get_wine(request: Request, page: int = 1, q: str = ''):
    wine, pagination = await get_items(request, 'wine', page)
    return {'wine': wine, 'pagination': pagination}


@router.get('/add_wine', name='add_wine')
async def add_wine_template(request: Request):
    return templates.TemplateResponse("wine/add_wine.html", {"request": request})
