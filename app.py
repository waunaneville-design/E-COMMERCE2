from flask import Flask, jsonify, request, abort, render_template
from storage import get_all_items, get_item, add_item, update_item, delete_item
from external_api import fetch_product

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def index():
    return render_template('index.html')


