from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


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
    page = 1 if page < 1 else page
    vodka, pagination = await request.app.mongo['vodka'].get_all(page=page)
    for v in vodka:
        v['_id'] = str(v['_id'])
        if not v.get('photos') or len(v['photos']['filenames']) == 0:
            v['avatar'] = request.url_for("photo", path='./vodka_default.jpg')
        else:
            v['avatar'] = request.url_for('photo', path=f"./vodka/{v['photos']['filenames'][0]}")
    pagination['prev_link'] = f'{request.url_for("get_vodka")}?page={page-1}'
    pagination['next_link'] = f'{request.url_for("get_vodka")}?page={page+1}'
    return {'vodka': vodka, 'pagination': pagination}


@router.get('/add_vodka', name='add_vodka')
async def add_vodka_template(request: Request):
    return templates.TemplateResponse("vodka/add_vodka.html", {"request": request})
