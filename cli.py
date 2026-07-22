"""CLI tool to interact with the Flask inventory API."""
import os

import click
import requests

BASE = os.environ.get('INVENTORY_API', 'http://127.0.0.1:5000')

def _request_with_error_handling(method, url, **kwargs):
    try:
        if method == 'GET':
            return requests.get(url, **kwargs)
        if method == 'POST':
            return requests.post(url, **kwargs)
        if method == 'PATCH':
            return requests.patch(url, **kwargs)
        if method == 'DELETE':
            return requests.delete(url, **kwargs)
        return requests.request(method, url, **kwargs)
    except requests.RequestException as exc:
        raise click.ClickException(f'API request failed: {exc}') from exc

@click.group()
def cli():
    """Inventory management CLI."""
    pass

@cli.command()
def list():
    """List all inventory items."""
    r = _request_with_error_handling('GET', f'{BASE}/inventory')
    r.raise_for_status()
    for it in r.json():
        click.echo(f"{it['id']}: {it['product_name']} (${it['price']}) stock={it['stock']}")


