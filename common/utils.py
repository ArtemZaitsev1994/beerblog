import os

from fastapi import Request


async def get_items(request: Request, section: str, page: int):
    page = 1 if page < 1 else page
    items, pagination = await request.app.mongo[section].get_all(page=page)
    for i in items:
        i['_id'] = str(i['_id'])
        if not i.get('photos') \
                or len(i['photos']['filenames']) == 0 \
                or not os.path.isfile(f"static/photo/{section}/{i['photos']['filenames'][0]}"):
            i['avatar'] = request.url_for("photo", path=f'./{section}_default.jpg')
        else:
            i['avatar'] = request.url_for('photo', path=f"./{section}/{i['photos']['filenames'][0]}")
    pagination['prev_link'] = request.url_for(f'get_{section}') + f'?page={page-1}'
    pagination['next_link'] = request.url_for(f'get_{section}') + f'?page={page+1}'

    return items, pagination
