from flask import request, jsonify
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
        client_id = request.args.get('client_id', None, type=int)
        data = {}
        if client_id:
            data = Feature.to_collection_dict(Feature.query.join(ClientPriority).filter_by(client_id=client_id).order_by(ClientPriority.priority.asc()), page, per_page, 'api.features')
        else:
            data = Feature.to_collection_dict(Feature.query.order_by(
                Feature.id.desc()), page, per_page, 'api.features')
        return jsonify(data)
    else:
        data = request.get_json()
        feature = Feature()
        feature.from_dict(data)
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
