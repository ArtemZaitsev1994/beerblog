from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/', name='common')
def beer_list(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
