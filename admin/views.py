from fastapi import APIRouter, Request

from admin.utils import get_items, get_item
from admin.scheme import ItemsList, ResponseBarItem, ResponseBeerItem, ResponseWineItem, Item, ChangeStateItem

router = APIRouter()
response_models = {
    'beer': ResponseBeerItem,
    'wine': ResponseWineItem,
    'bar': ResponseBarItem
}


@router.post('/admin_panel_list', name='admin_panel_list')
async def admin_panel_list(request: Request):
    items = [
        {'itemType': k, 'notConfirmed': await v.count_not_confirmed(), 'total': await v.count_all()}
        for k, v
        in request.app.mongo.items()
    ]
    return {'success': True, 'items': items}


@router.post('/{item_type}', name='get_items_list')
async def get_items_list(item_type, request: Request, settings: ItemsList):
    response = {'success': False}
    if item_type not in request.app.mongo:
        response['message'] = 'Wrong item\'s type.'
        return response
    items, pagination = await get_items(request, item_type, **settings.dict())

    return {'success': True, 'items': items, 'pagination': pagination}


@router.post('/{item_type}/get_item', name='admin_get_item')
async def admin_get_item(item_type, request: Request, item: Item):
    item = await get_item(request, item_type, item.id)
    return response_models[item_type](**item).dict()


@router.post('/{item_type}/change_item_state', name='change_item_state')
async def change_item_state(item_type, request: Request, item: ChangeStateItem):
    result = await request.app.mongo[item_type].change_item_state(item.id, item.not_confirmed)

    if result.acknowledged:
        response = {'success': True}
    else:
        response = {
            'success': False,
            'message': 'Error with db.'
        }
    return response


@router.post('/{item_type}/delete_item', name='delete_item')
async def delete_item(item_type, request: Request, item: Item):
    result = await request.app.mongo[item_type].delete_item(item.id)

    if result.deleted_count == 1:
        response = {'success': True}
    else:
        response = {
            'success': False,
            'message': 'Error with db.'
        }
    return response
