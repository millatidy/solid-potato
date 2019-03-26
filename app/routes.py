from app import app
from .models import *
from flask import request, jsonify


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Client.to_collection_dict(Client.query, page, per_page, 'clients')
        return jsonify(data)
    else:
        data = request.get_json()
        client = Client()
        client.name = data['name']
        client.save()
        return jsonify(client.to_dict())

@app.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    if request.method == 'GET':
        client = Client()
        client = client.find_one(id)
        return jsonify(client.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        client = Client()
        client.id = data['id']
        client.name = data['name']
        client = client.update()
        return jsonify(client.to_dict())
    else:
        data = request.get_json()
        client = Client()
        client.id = data['id']
        client.delete()
        return jsonify({'message': 'client deleted'})


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
def get_requests(id):
    pass

@app.route('/feature-requests', methods=['GET', 'POST'])
def feature_requests():
    pass

@app.route('/feature-requests/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def feature_request(id):
    pass