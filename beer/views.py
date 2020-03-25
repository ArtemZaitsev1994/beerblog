from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/', name='beer')
async def beer_list(request: Request, page: int = 1):
    return templates.TemplateResponse("beer.html", {"request": request, "id": id})


@router.get('/add_beer', name='add_beer')
async def add_beer_template(request: Request):
    return templates.TemplateResponse("add_beer.html", {"request": request})


@router.post('/add_beer', name='add_beer')
async def add_beer(*, name: str=Form(...)):
    print(name)
    pass
