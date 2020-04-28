from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


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
    wine, pagination = await request.app.mongo['wine'].get_all(page=page)
    for b in wine:
        b['_id'] = str(b['_id'])
        if not b.get('photos') or len(b['photos']['filenames']) == 0:
            b['avatar'] = request.url_for("photo", path='./wine/wine_default.png')
        else:
            b['avatar'] = request.url_for('photo', path=f"./wine/{b['photos']['filenames'][0]}")
    pagination['prev_link'] = request.url_for('get_wine') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_wine') + f'?page={page+1}'
    return {'wine': wine, 'pagination': pagination}


@router.get('/add_wine', name='add_wine')
async def add_wine_template(request: Request):
    return templates.TemplateResponse("wine/add_wine.html", {"request": request})
