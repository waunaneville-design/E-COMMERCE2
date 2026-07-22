"""CLI tool to interact with the Flask inventory API."""
import os

import click
import requests

BASE = os.environ.get('INVENTORY_API', 'http://127.0.0.1:5000')


