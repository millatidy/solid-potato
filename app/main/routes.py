from flask import render_template
from app.main import bp

@bp.route('/')
def index_page():
    return render_template('features.html')

@bp.route('/client')
def clients_page():
    return render_template('clients.html')

@bp.route('/client/<int:id>')
def client_detials_page(id):
    return render_template('client_details.html')

@bp.route('/feature/<int:id>')
def feature_deatils_page(id):
    return render_template('feature_details.html')