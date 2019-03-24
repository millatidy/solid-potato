from app import db
from flask import abort
from datetime import datetime, timedelta

class DAO(object):

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class DAO_UNIQUE_NAME(DAO):

    def save(self):
        if not self.is_unique():
            self.name += "_1"
        db.session.add(self)
        db.session.commit()    

    def is_unique(self):
        if self.query.filter_by(name=self.name).count() > 0:
            return False
        return True


class Client(DAO_UNIQUE_NAME, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)


class ProductArea(DAO_UNIQUE_NAME, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)


class Feature(DAO, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(300))
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)

    def save(self):
        if not self.is_unique():
            self.title += "_1"
        db.session.add(self)
        db.session.commit()    

    def is_unique(self):
        if self.query.filter_by(title=self.title).count() > 0:
            return False
        return True


class FeatureRequest(DAO, db.Model):
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime(), default=datetime.utcnow() + timedelta(days=90))
