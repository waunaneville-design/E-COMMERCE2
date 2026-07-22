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
