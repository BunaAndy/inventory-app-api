item_schema = {
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