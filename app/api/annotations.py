from functools import wraps
from flask import request, jsonify

def feature_request_checker(f):
    @wraps(f)
    def _args_checker(*args, **kwargs):
        feature_id = request.args.get('feature_id', None, type=int)
        client_id = request.args.get('client_id', None, type=int)

        r_args = (int(feature_id != None), int(client_id != None))

        if r_args == (0, 0):
            return jsonify({'message': 'feature_id and client_id cannot be empty'})

        if (r_args[0] != r_args[1]):
            return jsonify({'message': 'both feature_id and client_id are required'})

        return f(feature_id, client_id, *args, **kwargs)

    return _args_checker


def paged_request(f):
    @wraps(f)
    def _get_pagination(*args, **kwargs):
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        page = request.args.get('page', 1, type=int)
        return f(page, per_page, *args, **kwargs)
    return _get_pagination
