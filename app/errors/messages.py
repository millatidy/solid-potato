from app.errors import bp

FILE_DELETED = {
	'message': 'File succesfully deleted',
	'status': 200
}

OBJECT_NOT_FOUND = {
	'message': 'Reqested file could be found',
	'status': 404
	}

MISSING_ID = {
	'message': 'Your request needs either feature_id or client_id set',
	'status': 400
}