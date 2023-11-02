from model.schemas.project_schema import project_schema

projects_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : project_schema,
        }
    },
    'required': [
        'Entries'
    ],
}