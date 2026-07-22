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

@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        abort(400, description='JSON body required')
    item = add_item(data)
    return jsonify(item), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def patch_inventory_item(item_id):
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        abort(400, description='JSON body required')
    item = update_item(item_id, data)
    if not item:
        abort(404, description='Item not found')
    return jsonify(item)

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory(item_id):
    ok = delete_item(item_id)
    if not ok:
        abort(404, description='Item not found')
    return jsonify({'deleted': item_id})

@app.route('/inventory/fetch', methods=['GET'])
def fetch_external():
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    if not barcode and not name:
        abort(400, description='Provide barcode or name')
    product = fetch_product(barcode=barcode, name=name)
    if not product:
        return jsonify({'status': 0, 'product': None}), 404
    return jsonify({'status': 1, 'product': product})

if __name__ == '__main__':
    app.run(debug=True)

