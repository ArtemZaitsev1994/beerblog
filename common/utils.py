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
    for i in items:
        i['_id'] = str(i['_id'])
        if not i.get('photos') \
                or len(i['photos']['filenames']) == 0 \
                or not os.path.isfile(f"photo/{section}/{i['photos']['filenames'][0]}"):
            i['avatar'] = request.url_for("static", path=f'./{section}_default.jpg')
        else:
            i['avatar'] = request.url_for('photo', path=f"./{section}/{i['photos']['filenames'][0]}")

        if not i.get('photos') \
                or i['photos'].get('avatar', '') == '' \
                or not os.path.isfile(f"photo/{section}/{i['photos']['avatar']}"):
            i['mini_avatar'] = request.url_for("static", path=f'./{section}_default_avatar.jpg')
        else:
            i['mini_avatar'] = request.url_for('photo', path=f"./{section}/{i['photos']['avatar']}")
    pagination['prev_link'] = request.url_for(f'get_{section}') + f'?page={page-1}'
    pagination['next_link'] = request.url_for(f'get_{section}') + f'?page={page+1}'

    return items, pagination
