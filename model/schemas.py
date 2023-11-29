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
        },
        'Manufacturer': {
            'type': 'string'
        }
    },
    'required': [
        'Barcode', 'Name', 'Quantity', 'Quantity Needed', 'Catalog', 'Manufacturer'
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
        },
        'BOM Added': {
            'type': 'boolean'
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
        },
        'Manufacturer': {
            'type': 'string'
        }
    },
    'required': [
        'Barcode', 'Name', 'Catalog', 'Manufacturer'
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

login_schema = {
    'type': 'object',
    'properties': {
        'Username': {
            'type': 'string'
        },
        'Password': {
            'type': 'string'
        }
    }
}