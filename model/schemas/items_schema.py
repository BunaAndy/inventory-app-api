from model.schemas.item_schema import item_schema

items_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : item_schema,
        }
    },
    'required': [
        'Entries'
    ],
}