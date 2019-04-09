from app import app
from .models import *
from .messages import *
from flask import request, jsonify, render_template
from datetime import datetime


@app.route('/')
def index_page():
    return render_template('index.html')


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

    if id is None:
        return jsonify(MISSING_ID)

    client = Client.query.get(id)

    if client is None:
            return jsonify(OBJECT_NOT_FOUND)

    if request.method == 'GET':
        return jsonify(client.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        client.name = data['name']
        db.session.commit()
        return jsonify(client.to_dict())

    else:
        db.session.delete(client)
        return jsonify(FILE_DELETED)


@app.route('/product-areas', methods=['GET', 'POST'])
def product_areas():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = ProductArea.to_collection_dict(ProductArea.query, page, per_page, 'product_areas')
        return jsonify(data)
    else:
        data = request.get_json()
        product_area = ProductArea()
        product_area.name = data['name']
        product_area.save()
        return jsonify(product_area.to_dict())

@app.route('/product-areas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product_area(id):
    if id is None:
        return jsonify(MISSING_ID)
    product_area = ProductArea.query.get(id)
    if product_area is None:
        return jsonify(OBJECT_NOT_FOUND)
    if request.method == 'GET':
        return jsonify(product_area.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        product_area.name = data['name']
        db.session.commit()
        return jsonify(product_area.to_dict())
    else:
        db.session.delete(product_area)
        db.session.commit()
        return jsonify(FILE_DELETED)

@app.route('/features', methods=['GET', 'POST'])
def features():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Feature.to_collection_dict(Feature.query, page, per_page, 'features')
        return jsonify(data)
    else:
        data = request.get_json()
        print(data)
        feature = Feature()
        feature.title = data['title']
        feature.description = data['description']
        feature.product_area_id = data['product_area_id']
        feature.save()
        return jsonify(feature.to_dict())

@app.route('/features/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def feature(id):
    if id is None:
        return jsonify(MISSING_ID)
    feature = Feature.query.get(id)
    if feature is None:
        return jsonify(OBJECT_NOT_FOUND)
    if request.method == 'GET':
        return jsonify(feature.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        feature.title = data['title']
        feature.description = data['description']
        feature.product_area_id = data['product_area_id']
        db.session.commit()
        return jsonify(feature.to_dict())
    else:
        db.session.delete(feature)
        db.session.commit()
        return jsonify(FILE_DELETED)

@app.route('/feature-requests', methods=['POST'])
def feature_requests():
    data = request.get_json()
    feature_request = FeatureRequest()
    feature_request.feature_id = data['feature_id']
    feature_request.client_id = data['client_id']
    feature_request.priority = data['priority']
    time_arr = data['target_date'].split("-")
    feature_request.target_date = datetime(int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
    feature_request.save()
    return jsonify(feature_request.to_dict())

@app.route('/feature-requests', methods=['GET'])
def get_feature_request():
    feature_id = request.args.get('feature_id', None, type=int)
    client_id = request.args.get('client_id', None, type=int)
    if (feature_id is None) and (client_id is None):
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = FeatureRequest.to_collection_dict(FeatureRequest.query, page, per_page, 'feature_requests')
        return jsonify(data)
    if request.method == 'GET':
        if feature_id and client_id:
            feature_request = FeatureRequest().query.get((feature_id, client_id))
            if feature_request is None:
                return jsonify(OBJECT_NOT_FOUND)
            return jsonify(feature_request.to_dict())
        else:
            data = {}
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            if feature_id:
                data = FeatureRequest.to_collection_dict(
                    FeatureRequest.query.filter_by(
                        feature_id=feature_id), page, per_page, 'get_feature_request', feature_id=feature_id)
            else:
                data = FeatureRequest.to_collection_dict(
                    FeatureRequest.query.filter_by(
                        client_id=client_id), page, per_page, 'get_feature_request', client_id=client_id)
            return jsonify(data)

@app.route('/feature-requests', methods=['PUT'])
def edit_feature_request():
    feature_id = request.args.get('feature_id', None, type=int)
    client_id = request.args.get('client_id', None, type=int)
    if (feature_id is None) and (client_id is None):
        return jsonify({'message': 'feature_id and client_id cannot be empty'})
    if (feature_id is None) or (client_id is None):
            return jsonify(MISSING_ID)
    if request.method == 'PUT':
        data = request.get_json()
        feature_request = FeatureRequest()
        feature_request.feature_id = data['feature_id']
        feature_request.client_id = data['client_id']
        feature_request = feature_request.query.get((feature_id, client_id))
        time_arr = data['target_date'].split("-")
        feature_request.target_date = datetime(int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
        feature_request.priority = data['priority']
        # feature_request.query.get((feature_id, client_id))
        db.session.commit()
        return jsonify(feature_request.to_dict())

@app.route('/feature-requests', methods=['DELETE'])
def delete_feature_request():
    feature_id = request.args.get('feature_id', None, type=int)
    client_id = request.args.get('client_id', None, type=int)
    if (feature_id is None) and (client_id is None):
        return jsonify({'message': 'feature_id and client_id cannot be empty'})
    if (feature_id is None) or (client_id is None):
            return jsonify(MISSING_ID)
    if request.method == 'DELETE':
        # data = request.get_json()
        # feature_id = data['feature_id']
        # client_id = data['client_id']
        feature_request = FeatureRequest().query.get((feature_id, client_id))
        db.session.delete(feature_request)
        db.session.commit()
        return jsonify(FILE_DELETED)

