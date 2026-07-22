"""In-memory mock database for inventory items.
Each item is a dict with at least: id, product_name, brands, barcode, ingredients_text, price, stock
"""

_items = [
    {
        'id': 1,
        'product_name': 'Organic Almond Milk',
        'brands': 'Silk',
        'barcode': '1234567890123',
        'ingredients_text': 'Filtered water, almonds, cane sugar',
        'price': 3.99,
        'stock': 24,
    },

 {
        'id': 2,
        'product_name': 'Whole Wheat Bread',
        'brands': 'Local Bakery',
        'barcode': '9876543210987',
        'ingredients_text': 'Whole wheat flour, water, yeast, salt',
        'price': 2.49,
        'stock': 12,
    },
]

def _next_id():
    if not _items:
        return 1
    return max(i['id'] for i in _items) + 1

def get_all_items():
    return list(_items)


def get_item(item_id):
    for it in _items:
        if it['id'] == item_id:
            return it
    return None

def add_item(data):
    item = {
        'id': _next_id(),
        'product_name': data.get('product_name') or data.get('name') or 'Unnamed Product',
        'brands': data.get('brands'),
        'barcode': data.get('barcode'),
        'ingredients_text': data.get('ingredients_text'),
        'price': float(data.get('price', 0.0)),
        'stock': int(data.get('stock', 0)),
    }
    _items.append(item)
    return item

def update_item(item_id, changes):
    item = get_item(item_id)
    if not item:
        return None
    # apply allowed changes
    for k in ('product_name', 'brands', 'barcode', 'ingredients_text'):
        if k in changes:
            item[k] = changes[k]
    if 'price' in changes:
        item['price'] = float(changes['price'])
    if 'stock' in changes:
        item['stock'] = int(changes['stock'])
    return item

def delete_item(item_id):
    global _items
    for i, it in enumerate(_items):
        if it['id'] == item_id:
            del _items[i]
            return True
    return False

def reset_items():
    """Helper for tests to reset to initial state."""
    global _items
    _items = [
        {
            'id': 1,
            'product_name': 'Organic Almond Milk',
            'brands': 'Silk',
            'barcode': '1234567890123',
            'ingredients_text': 'Filtered water, almonds, cane sugar',
            'price': 3.99,
            'stock': 24,
        },
        {
            'id': 2,
            'product_name': 'Whole Wheat Bread',
            'brands': 'Local Bakery',
            'barcode': '9876543210987',
            'ingredients_text': 'Whole wheat flour, water, yeast, salt',
            'price': 2.49,
            'stock': 12,
        },
    ]
