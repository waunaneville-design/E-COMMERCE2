import json
import pytest

from external_api import fetch_product


def test_fetch_product_by_name(monkeypatch):
    # mock requests.get inside external_api
    class DummyResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'products': [{'product_name': 'Test', 'brands': 'B', 'code': '000', 'ingredients_text': 'i'}]}

    def fake_get(url, params=None, timeout=5):
        return DummyResp()

    monkeypatch.setattr('external_api.requests.get', fake_get)
    p = fetch_product(name='Test')
    assert p['product_name'] == 'Test'


def test_fetch_product_by_barcode(monkeypatch):
    class DummyResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'status': 1, 'product': {'product_name': 'Milk', 'brands': 'B', 'code': '111', 'ingredients_text': 'i'}}

    def fake_get(url, timeout=5):
        return DummyResp()

    monkeypatch.setattr('external_api.requests.get', fake_get)
    p = fetch_product(barcode='111')
    assert p['product_name'] == 'Milk'
