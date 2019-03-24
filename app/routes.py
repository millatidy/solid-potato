from app import app
from .models import *
from flask import request, jsonify


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        clients = []
        client = Client()
        clients = client.find_all()
        return jsonify(clients)
    else:
        data = request.get_json()
        client = Client()
        client.name = data['name']
        client.save()
        return jsonify({"id": client.id, "name": client.name})

@app.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    pass

@app.route('/product-areas', methods=['GET', 'POST'])
def product_areas():
    pass

@app.route('/product-areas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product_area(id):
    pass

@app.route('/features', methods=['GET', 'POST'])
def features():
    pass

@app.route('/features/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def feature(id):
    pass

@app.route('/feature-requests', methods=['GET', 'POST'])
def feature_requests():
    pass

@app.route('/feature-requests/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def feature_request(id):
    pass