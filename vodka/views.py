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


@router.get('/', name='vodka')
async def vodka_list(request: Request):
    # await request.app.mongo['vodka'].clear_db()
    return templates.TemplateResponse("vodka/vodka.html", {"request": request})


@router.post('/get_vodka', name='get_vodka')
async def get_vodka(request: Request, page: int = 1, q: str = ''):
    vodka, pagination = await get_items(request, 'vodka', page)
    return {'vodka': vodka, 'pagination': pagination}


@router.get('/add_vodka', name='add_vodka')
async def add_vodka_template(request: Request):
    return templates.TemplateResponse("vodka/add_vodka.html", {"request": request})
