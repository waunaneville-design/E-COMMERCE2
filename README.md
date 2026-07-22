# Inventory Management API

A Flask-based inventory management app with a React-powered frontend, an in-memory mock database, and OpenFoodFacts integration. It includes a CLI for interacting with the API and unit tests for core behavior.

## Features

- React frontend served from the Flask app at `/`
- CRUD operations for inventory items via REST API
- External product lookup by barcode or name
- CLI commands for listing, adding, viewing, updating, deleting, and fetching items
- Basic error handling for invalid input and API failures

## Installation

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

Then open http://127.0.0.1:5000/ to use the React frontend.

## CLI

Set `INVENTORY_API` if the API runs on a different host/port. Example commands:

```bash
python cli.py list
python cli.py add --name "New Product" --price 1.99 --stock 10
python cli.py view 1
python cli.py update 1 --price 2.49
python cli.py delete 1
python cli.py fetch --barcode 1234567890123
```

## API Endpoints

- `GET /inventory` -> returns all items
- `GET /inventory/<id>` -> returns a single item or 404
- `POST /inventory` -> create item (JSON body)
- `PATCH /inventory/<id>` -> partial update (JSON body)
- `DELETE /inventory/<id>` -> delete an item
- `GET /inventory/fetch?barcode=...&name=...` -> fetch product data from OpenFoodFacts

## Notes

- Storage is simulated via an in-memory array in `storage.py`.
- Tests are in `tests/` and mock external calls.
