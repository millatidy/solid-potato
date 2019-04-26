import os
import unittest

from coverage import coverage
basedir = os.getcwd()
cov = coverage(branch=True, omit=['.git/*', 'venv/*', 'tests.py', 'requirements.txt'])
cov.start()

from flask import current_app, json
from app import create_app, db
from datetime import datetime
from app.models import *
from app.api.routes import *
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None

class ClientCase(unittest.TestCase):

    def setUp(self):
        # self.app = create_app(TestConfig)
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        db.create_all()

class ErrorsCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



class APICase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_search(self):
    #     res = search().get("?q=milla")
    #     print(res)

    def test_get_clients(self):
        res = clients()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 0)
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        res = clients()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 1)

    def test_post_client(self):
        res = self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Client A")

    def test_get_client(self):
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        res = self.test_client.get('/api/clients/1')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Client A")

    def test_edit_client(self):
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        res = self.test_client.put('/api/clients/1', data=json.dumps(dict(name="Client B")), content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Client B")

    def test_delete_client(self):
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        res = self.test_client.delete('/api/clients/1')
        self.assertEqual(res.status_code, 200)

    def test_get_product_areas(self):
        res = product_areas()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 0)
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        res = product_areas()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 1)

    def test_post_product_area(self):
        res = self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Billing")

    def test_get_product_area(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        res = self.test_client.get('/api/product-areas/1')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Billing")

    def test_edit_product_area(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        res = self.test_client.put('/api/product-areas/1', data=json.dumps(dict(name="Policies")), content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['name'], "Policies")

    def test_delete_product_area(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        res = self.test_client.delete('/api/product-areas/1')
        self.assertEqual(res.status_code, 200)

    def test_get_features(self):
        res = features()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 0)
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        self.test_client.post('/api/features', data=json.dumps(dict(title="Feature_1", client_id=1, client_priority=1, description="The Feature", product_area_id=1)), content_type='application/json')
        res = features()
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(data['items']), 1)

    def test_get_feature(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        self.test_client.post('/api/features', data=json.dumps(dict(title="Feature_1", client_id=1, client_priority=1, description="The Feature", product_area_id=1)), content_type='application/json')
        res = self.test_client.get('/api/features/1')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['title'], "Feature_1")

    def test_edit_feature(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        self.test_client.post('/api/features', data=json.dumps(dict(title="Feature_1", client_id=1, client_priority=9,description="The Feature", product_area_id=1)), content_type='application/json')
        res = self.test_client.put('/api/features/1', data=json.dumps(dict(title="Feature 2", client_id=1, client_priority=8, description="The Feature", product_area_id=1)), content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['title'], "Feature 2")

    def test_delete_feature(self):
        self.test_client.post('/api/product-areas', data=json.dumps(dict(name="Billing")), content_type='application/json')
        self.test_client.post('/api/clients', data=json.dumps(dict(name="Client A")), content_type='application/json')
        self.test_client.post('/api/features', data=json.dumps(dict(title="Feature_1", client_id=1, client_priority=8, description="The Feature", product_area_id=1)), content_type='application/json')
        res = self.test_client.delete('/api/features/1')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    try:
        unittest.main(verbosity=2)
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\mCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
