from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify, request, current_app
from app.api import bp
from app import db

"""This module captures all application errors and returns
   custom responses
"""

def error_resposnse(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Uknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

@bp.app_errorhandler(400)
def bad_request(ex):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Bad request.", "code":"400"})
    else:
        return ex

@bp.app_errorhandler(404)
def not_found(ex):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resources not found.", "code":"404"})
    else:
        return ex

@bp.app_errorhandler(405)
def method_not_allowed(ex):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Method not allowed.", "code":"405"})
    else:
        return ex

# if we ever fake delete stuff
@bp.app_errorhandler(410)
def gone(ex):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource is gone.", "code":"410"})
    else:
        return ex


@bp.app_errorhandler(500)
def internal_server_error(ex):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error.", "code":"500"})
    else:
        return ex
