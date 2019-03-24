import os
import unittest

from coverage import coverage
basedir = os.getcwd()
cov = coverage(branch=True, omit=['.git/*', 'venv/*', 'tests.py', 'requirements.txt'])
cov.start()


from app import app, db
from app.models import *

class DAOCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

        self.client = Client()
        self.client.name = "Client A"
        self.client.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        client = Client()
        client.name = "Client B"
        client.save()
        self.assertEqual(self.client.id, 1)
        self.assertEqual(client.id, 2)

    def test_unique(self):
        client = Client()
        client.name = "Client A"
        client.save()
        self.assertNotEqual(client.name, self.client.name)
        self.assertEqual(client.name, "Client A_1")

    def test_update(self):
        client = Client.query.get(1)
        client.name = "Client X"
        client.update()
        self.assertEqual(client.name, "Client X")
        self.assertNotEqual(client.name, "Client A")

    def test_delete(self):
        client = Client.query.get(1)
        client.delete()
        clients = len(db.session.query(Client).all())
        self.assertNotEqual(clients, 1)
        self.assertEqual(clients, 0)

class PriorityCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

        client_A = Client()
        client_A.name = "Client A"
        client_A.save()

        productArea = ProductArea()
        productArea.title = "Policies"
        productArea.save()

        feature_X = Feature()
        feature_X.title = "The next big thing"
        feature_X.description = "Lorem ipsum dolor sit amet"
        feature_X.product_area_id = productArea.id
        feature_X.save()

        feature_request = FeatureRequest()
        feature_request.feature_id = feature_X.id
        feature_request.client_id = client_A.id
        feature_request.priority = 4
        feature_request.save()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    '''
        Business requirement:
        - Priority numbers should not repeat for the given client
    '''
    def test_priority_numbering(self):
        feature_request = FeatureRequest().query.get((1,1))
        feature_request.priority = 3
        feature_request.update()
        self.assertNotEqual(feature_request.priority, 4)
        self.assertEqual(feature_request.priority, 3)



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