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

@cli.command()
@click.option('--name', prompt=True)
@click.option('--price', type=float, default=0.0)
@click.option('--stock', type=int, default=0)
def add(name, price, stock):
    """Add a new inventory item."""
    payload = {'product_name': name, 'price': price, 'stock': stock}
    r = _request_with_error_handling('POST', f'{BASE}/inventory', json=payload)
    r.raise_for_status()
    click.echo('Added: ' + str(r.json()))

@cli.command()
@click.argument('item_id', type=int)
def view(item_id):
    """View a single inventory item."""
    r = _request_with_error_handling('GET', f'{BASE}/inventory/{item_id}')
    if r.status_code == 404:
        click.echo('Not found')
        return
    r.raise_for_status()
    click.echo(r.json())

@cli.command()
@click.argument('item_id', type=int)
@click.option('--price', type=float)
@click.option('--stock', type=int)
def update(item_id, price, stock):
    """Update an inventory item."""
    payload = {}
    if price is not None:
        payload['price'] = price
    if stock is not None:
        payload['stock'] = stock
    if not payload:
        click.echo('Nothing to update')
        return
    r = _request_with_error_handling('PATCH', f'{BASE}/inventory/{item_id}', json=payload)
    if r.status_code == 404:
        click.echo('Not found')
        return
    r.raise_for_status()
    click.echo('Updated: ' + str(r.json()))

