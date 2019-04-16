from flask import request, jsonify, render_template
from datetime import datetime
from app import db
from app.models import *
from app.messages import *
from app.api import bp
from app.api.annotations import feature_request_checker, paged_request


@bp.route('/search')
@paged_request
def search(page, per_page):
    """Search endpoint for the api

       example:
                /search?q="search query"
    """
    query = request.args.get('q')
    features_query, total = Feature.search(query, page, 10)
    features = Feature.to_collection_dict(
        features_query, page, per_page, 'api.features')
    return jsonify(features)


@bp.route('/clients', methods=['GET', 'POST'])
@paged_request
def clients(page, per_page):
    if request.method == 'GET':
        data = Client.to_collection_dict(
            Client.query, page, per_page, 'api.clients')
        return jsonify(data)
    else:
        data = request.get_json()
        client = Client()
        client.name = data['name']
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict())


@bp.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    client = Client.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(client.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        client.name = data['name']
        db.session.commit()
        return jsonify(client.to_dict())
    else:
        db.session.delete(client)
        db.session.commit()
        return jsonify(FILE_DELETED)


@bp.route('/product-areas', methods=['GET', 'POST'])
@paged_request
def product_areas(page, per_page):
    if request.method == 'GET':
        data = ProductArea.to_collection_dict(
            ProductArea.query, page, per_page, 'api.product_areas')
        return jsonify(data)
    else:
        data = request.get_json()
        product_area = ProductArea()
        product_area.name = data['name']
        db.session.add(product_area)
        db.session.commit()
        return jsonify(product_area.to_dict())


@bp.route('/product-areas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product_area(id):
    product_area = ProductArea.query.get_or_404(id)

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


@bp.route('/features', methods=['GET', 'POST'])
@paged_request
def features(page, per_page):
    if request.method == 'GET':
        data = Feature.to_collection_dict(Feature.query.order_by(
            Feature.id.desc()), page, per_page, 'api.features')
        return jsonify(data)
    else:
        data = request.get_json()
        feature = Feature()
        feature.title = data['title']
        feature.description = data['description']
        feature.product_area_id = data['product_area_id']
        db.session.add(feature)
        db.session.commit()
        return jsonify(feature.to_dict())


@bp.route('/features/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def feature(id):
    feature = Feature.query.get_or_404(id)
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


@bp.route('/feature-requests', methods=['GET'])
@paged_request
def get_feature_request(page, per_page):
    feature_id = request.args.get('feature_id', None, type=int)
    client_id = request.args.get('client_id', None, type=int)

    args = (int(feature_id is not None), int(client_id is not None))

    # both feature_id and client_id are None
    if args == (0, 0):
        data = FeatureRequest.to_collection_dict(
            FeatureRequest.query, page, per_page, 'api.feature_requests')
        return jsonify(data)

    # feature_id is None
    if args == (0, 1):
        data = FeatureRequest.to_collection_dict(
            FeatureRequest.query.filter_by(
                client_id=client_id),
            page,
            per_page,
            'api.get_feature_request',
            client_id=client_id)
        return jsonify(data)

    # client_id is None
    if args == (1, 0):
        data = FeatureRequest.to_collection_dict(
            FeatureRequest.query.filter_by(
                feature_id=feature_id),
            page,
            per_page,
            'api.get_feature_request',
            feature_id=feature_id)
        return jsonify(data)

    if args == (1, 1):
        feature_request = FeatureRequest().query.get_or_404((feature_id, client_id))
        return jsonify(feature_request.to_dict())


@bp.route('/feature-requests', methods=['POST'])
def feature_requests():
    data = request.get_json()
    feature_request = FeatureRequest()
    feature_request.feature_id = data['feature_id']
    feature_request.client_id = data['client_id']
    feature_request.priority = data['priority']
    time_arr = data['target_date'].split("-")
    feature_request.target_date = datetime(
        int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
    db.session.add(feature_request)
    db.session.commit()
    return jsonify(feature_request.to_dict())


@bp.route('/feature-requests', methods=['PUT'])
@feature_request_checker
def edit_feature_request(feature_id, client_id):
    data = request.get_json()
    feature_request = FeatureRequest.query.get((feature_id, client_id))
    time_arr = data['target_date'].split("-")
    feature_request.target_date = datetime(
        int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))
    feature_request.priority = data['priority']
    db.session.commit()
    return jsonify(feature_request.to_dict())


@bp.route('/feature-requests', methods=['DELETE'])
@feature_request_checker
def delete_feature_request(feature_id, client_id):
    feature_request = FeatureRequest.query.get_or_404((feature_id, client_id))
    db.session.delete(feature_request)
    db.session.commit()
    return jsonify(FILE_DELETED)
