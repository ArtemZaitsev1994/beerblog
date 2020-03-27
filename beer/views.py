import graphene
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.graphql import GraphQLApp


templates = Jinja2Templates(directory="templates")
router = APIRouter()


class CommonResponse(BaseModel):
    success: bool
    message: str = None
    error_data: str = None


@router.get('/', name='beer')
async def beer_list(request: Request, page: int = 1):
    return templates.TemplateResponse("beer.html", {"request": request, "id": id})


@router.get('/add_beer', name='add_beer')
async def add_beer_template(request: Request):
    return templates.TemplateResponse("add_beer.html", {"request": request})


class BeerDataIn(BaseModel):
    name: str
    rate: int
    manufacturer: str = None
    fortress: int = None
    gravity: int = None
    review: str = None
    others: str = None


@router.post('/add_beer', name='add_beer', response_model=CommonResponse)
async def add_beer(request: Request, *, data: BeerDataIn):
    result = await request.app.mongo['beer'].insert_item(data.to_dict())
    if result.acknowledged:
        return {'acknowledged': True}
    else:
        return {'acknowledged': False, 'message': 'Insert failed', 'error_data': data}


class CreateBeer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        rate: int
        manufacturer = graphene.String()
        fortress: int = None
        gravity: int = None
        review = graphene.String()
        others = graphene.String()

    def


class Mutation(graphene.ObjectType):
    beer = CreateBeer.Field()

    async def resolve_addBeer(self, info, request: Request, *, data: BeerDataIn):
        pass


router.add_route('/beer_query', GraphQLApp(schema=graphene.Schema(mutation=Mutation)))
