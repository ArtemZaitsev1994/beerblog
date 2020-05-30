from typing import Dict, Any
import os

from fastapi import Request
from pymongo import ASCENDING, DESCENDING


SORTING = {
    'time_desc': ('_id', DESCENDING),
    'time_asc': ('_id', ASCENDING),
    'rate_desc': ('rate', DESCENDING),
    'rate_asc': ('rate', ASCENDING),
}


async def get_items(request: Request, section: str, page: int, sorting: str = ''):
    sorting = SORTING.get(sorting, SORTING['time_desc'])
    page = 1 if page < 1 else page
    items, pagination = await request.app.mongo[section].get_all(page=page, sorting=sorting)
    items = [format_item(request, i, section) for i in items]

    _url = request.url_for(f'get_{section}')
    pagination['prev_link'] = f'{_url}?page={page-1}'
    pagination['next_link'] = f'{_url}?page={page+1}'

    return items, pagination


async def get_item(request: Request, section: str, _id: str):
    item = await request.app.mongo[section].get_item(_id=_id)
    return format_item(request, item, section)


def format_item(request: Request, item: Dict[str, Any], section: str):
    item['_id'] = str(item['_id'])
    if not item.get('photos') \
            or len(item['photos']['filenames']) == 0 \
            or not os.path.isfile(f"photo/{section}/{item['photos']['filenames'][0]}"):
        item['avatar'] = request.url_for("static", path=f'./{section}_default.jpg')
    else:
        item['avatar'] = request.url_for('photo', path=f"./{section}/{item['photos']['filenames'][0]}")

    if not item.get('photos') \
            or item['photos'].get('avatar', '') == '' \
            or not os.path.isfile(f"photo/{section}/{item['photos']['avatar']}"):
        item['mini_avatar'] = request.url_for("static", path=f'./{section}_default_avatar.jpg')
    else:
        item['mini_avatar'] = request.url_for('photo', path=f"./{section}/avatars/{item['photos']['avatar']}")

    return item
