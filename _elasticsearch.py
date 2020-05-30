from elasticsearch_async import AsyncElasticsearch
from fastapi import FastAPI


ES_INDICES = {
    'beer': {
        'mappings': {
            'properties': {
                'mongo_id': {'type': 'keyword'},
                'name': {'type': 'keyword'},
                'rate': {'type': 'integer'},
                'manufacturer': {'type': 'keyword'},
                'review': {'type': 'text', 'analyzer': 'russian'},
                'others': {'type': 'text', 'analyzer': 'russian'},
                'fortress': {'type': 'float'},
                'ibu': {'type': 'integer'},
                'alcohol': {'type': 'float'}
            }
        }
    },
    'vodka': {
        'mappings': {
            'properties': {
                'mongo_id': {'type': 'keyword'},
                'name': {'type': 'keyword'},
                'rate': {'type': 'integer'},
                'manufacturer': {'type': 'keyword'},
                'review': {'type': 'text', 'analyzer': 'russian'},
                'others': {'type': 'text', 'analyzer': 'russian'}
            }
        }
    },
    'wine': {
        'mappings': {
            'properties': {
                'mongo_id': {'type': 'keyword'},
                'name': {'type': 'keyword'},
                'rate': {'type': 'integer'},
                'manufacturer': {'type': 'keyword'},
                'review': {'type': 'text', 'analyzer': 'russian'},
                'others': {'type': 'text', 'analyzer': 'russian'},
                'sugar': {'type': 'text'},
                'style': {'type': 'text'},
                'alcohol': {'type': 'float'}
            }
        }
    }
}


async def setup_es(app: FastAPI):
    app.es_client = AsyncElasticsearch(hosts=['localhost'])

    indices = ['beer', 'vodka', 'wine']
    for index in indices:
        if not await app.es_client.indices.exists(index=index):
            await app.es_client.indices.create(index=index, body=ES_INDICES[index])
        # await app.es_client.indices.delete(index=index, ignore=[400, 404])
