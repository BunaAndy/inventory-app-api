from item_schema import item_schema

entries_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : item_schema,
        },
        'Project': {
            'type': 'string'
        }
    },
    'required': [
        'Entries', 'Project'
    ],
}