from project_schema import project_schema

entry_schema = {
    'type': 'object',
    'properties': {
        'Projects' : {
            'type' : 'array',
            'items' : project_schema,
        }
    },
    'required': [
        'Entries'
    ],
}