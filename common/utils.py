from typing import Dict, Any
import os

from fastapi import Request
from pymongo import ASCENDING, DESCENDING
from aiofile import AIOFile
from uuid import uuid4
from PIL import Image
import jwt

from settings import JWT_ALGORITHM, JWT_SECRET_KEY


SORTING = {
    'time_desc': ('_id', DESCENDING),
    'time_asc': ('_id', ASCENDING),
    'rate_desc': ('rate', DESCENDING),
    'rate_asc': ('rate', ASCENDING),
}


async def get_items(request: Request, section: str, page: int, sorting: str = '', search_query: str = ''):
    sorting = SORTING.get(sorting, SORTING['time_desc'])
    page = 1 if page < 1 else page
    items, pagination = await request.app.mongo[section].get_all(page=page, sorting=sorting, query=search_query)
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
            or not os.path.isfile(f"photo/{section}/avatars/{item['photos']['avatar']}"):
        item['mini_avatar'] = request.url_for("static", path=f'./{section}_default_avatar.jpg')
    else:
        item['mini_avatar'] = request.url_for('photo', path=f"./{section}/avatars/{item['photos']['avatar']}")

    return item


async def save_item_to_base(request: Request, item: Dict[str, Any], section: str):
    photo_dir = request.app.photo_path[section]

    # велосипед
    token = request.headers['Authorization']
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    item['postedBy'] = payload['login']
    item['rates'] = {
        item['postedBy']: item['rate']
    }
    item['search_by_name'] = item['name'].lower()

    filenames = []
    for photo in item['photos']:
        if photo.filename == '':
            break
        filename = uuid4().hex
        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir)
        image_path = os.path.join(photo_dir, filename)
        async with AIOFile(image_path, 'wb') as f:
            await f.write(await photo.read())
        filenames.append(filename)

    avatar_name = ''
    if len(filenames) > 0:
        avatar_dir = os.path.join(photo_dir, "avatars/")
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)
        avatar = Image.open(image_path)
        buff_size = avatar.size[0] // 40
        h, w = int(avatar.size[0] / buff_size), int(avatar.size[1] / buff_size)
        avatar = avatar.resize((h, w), Image.ANTIALIAS)
        avatar_path = os.path.join(avatar_dir, f'avatar_{filename}.png')
        avatar = avatar.save(avatar_path, quality=30)
        avatar_name = f'avatar_{filenames[0]}.png'

    item['photos'] = {
        'filenames': filenames,
        'avatar': avatar_name
    }

    result = await request.app.mongo[section].insert_item(item)

    if result.acknowledged:
        response = {'success': True}
    else:
        response = {
            'success': False,
            'message': 'Insert failed at the serverside. Call Тёма, scream and run around',
            'error_data': item
        }
    return response
