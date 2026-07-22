import pytest
import requests
from click.testing import CliRunner

import cli as cli_module
from storage import reset_items, get_all_items


class DummyResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_storage_reset():
    reset_items()
    items = get_all_items()
    assert len(items) >= 2


def test_cli_list_handles_api_failure(monkeypatch):
    runner = CliRunner()

    def fake_get(*args, **kwargs):
        raise requests.RequestException('boom')

    monkeypatch.setattr(cli_module.requests, 'get', fake_get)

    result = runner.invoke(cli_module.cli, ['list'])

    assert result.exit_code != 0
    assert 'API request failed' in result.output


def test_cli_view_returns_not_found(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(cli_module.requests, 'get', lambda *args, **kwargs: DummyResponse(404, {'error': 'not found'}))

    result = runner.invoke(cli_module.cli, ['view', '999'])

    assert result.exit_code == 0
    assert 'Not found' in result.output
