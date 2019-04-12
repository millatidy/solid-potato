from flask import render_template
from app.main import bp


@bp.route('/')
@bp.route('/features')
def index_page():
    return render_template('features.html')


@bp.route('/clients')
def clients_page():
    return render_template('clients.html')


@bp.route('/clients/<int:id>')
def client_detials_page(id):
    return render_template('client_details.html')


@bp.route('/features/<int:id>')
def feature_deatils_page(id):
    return render_template('feature_details.html')


@bp.route('/search')
def search_results_page():
    return render_template('search_results.html')


@bp.route('/about')
def about_page():
	return render_template('about_page.html')
