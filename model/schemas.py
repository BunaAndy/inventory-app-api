project_item_schema = {
    'type': 'object',
    'properties' : {
        'Barcode': {
            'type' : 'string'
        },
        'Name': {
            'type' : 'string'
        },
        'Quantity': {
            'type' : 'integer'
        },
        'Quantity Needed': {
            'type' : 'integer'
        },
        'Catalog': {
            'type': 'string'
        }
    },
    'required': [
        'Barcode', 'Name', 'Quantity', 'Quantity Needed', 'Catalog'
    ]
}

project_items_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : project_item_schema,
        }
    },
    'required': [
        'Entries'
    ],
}

project_schema = {
    'type': 'object',
    'properties': {
        'Project Number': {
            'type': 'string'
        },
        'Project Name': {
            'type': 'string'
        }
    },
    'required': [
        'Project Number', 'Project Name'
    ]
}

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

item_schema = {
    'type': 'object',
    'properties' : {
        'Barcode': {
            'type' : 'string'
        },
        'Name': {
            'type' : 'string'
        },
        'Catalog': {
            'type': 'string'
        }
    },
    'required': [
        'Barcode', 'Name', 'Catalog'
    ]
}

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

modify_project_items_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : {
                'type' : 'array',
                'items' : {
                    'type' : project_item_schema
                }
            }
        }
    },
    'required': [
        'Entries'
    ],
}

modify_items_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : {
                'type' : 'array',
                'items' : {
                    'type' : item_schema
                }
            }
        }
    },
    'required': [
        'Entries'
    ],
}

modify_projects_schema = {
    'type': 'object',
    'properties': {
        'Entries' : {
            'type' : 'array',
            'items' : {
                'type' : 'array',
                'items' : {
                    'type' : project_schema
                }
            }
        }
    },
    'required': [
        'Entries'
    ],
}