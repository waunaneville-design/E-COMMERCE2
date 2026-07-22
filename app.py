from flask import Flask, jsonify, request, abort, render_template
from storage import get_all_items, get_item, add_item, update_item, delete_item
from external_api import fetch_product

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory', methods=['GET'])
def list_inventory():
    """GET /inventory -> returns list of all items"""
    return jsonify(get_all_items())

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = get_item(item_id)
    if not item:
        abort(404, description='Item not found')
    return jsonify(item)

