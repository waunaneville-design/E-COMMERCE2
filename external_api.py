"""Simple OpenFoodFacts integration. Returns a normalized product dict or None."""
from socket import timeout
from unicodedata import name

import requests

def _normalize_of_product(of_product):
    # Map a few fields into our internal shape
    return {
        'product_name': of_product.get('product_name'),
        'brands': of_product.get('brands'),
        'barcode': of_product.get('code') or of_product.get('barcode'),
        'ingredients_text': of_product.get('ingredients_text'),
    }

def fetch_product(barcode=None, name=None, timeout=5):
    """Fetch product data from OpenFoodFacts by barcode or search by name.

    Returns normalized product dict or None on failure.
    """
    try:
        if barcode:
            url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get('status') == 1 and data.get('product'):
                return _normalize_of_product(data['product'])
            return None

        if name:
            params = {'search_terms': name, 'search_simple': 1, 'json': 1, 'page_size': 1}
            url = 'https://world.openfoodfacts.org/cgi/search.pl'
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            products = data.get('products') or []
            if products:
                return _normalize_of_product(products[0])
            return None
    except Exception:
        return None

