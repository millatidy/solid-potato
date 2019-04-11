from app import db
from app.search import add_to_index, remove_from_index, query_index
from flask import abort, url_for
from datetime import datetime, timedelta

class DAO(object):

    @classmethod        
    def find_all(cls):
        return cls.query.all()

    def find_one(self, id):
        return self.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self = self.query.get(self.id)
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

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total 

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj.__tablename__, obj):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Client(PaginatedAPIMixin, DAO_UNIQUE_NAME, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    requests = db.relationship('FeatureRequest', cascade='all, delete, delete-orphan', lazy='dynamic', backref='client')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'no_requests': self.requests.count(),
            'links': {
                'self': url_for('client', id=self.id),
                'requests': url_for('get_feature_request', client_id=self.id)
            }
        }
        return data


class ProductArea(PaginatedAPIMixin, DAO_UNIQUE_NAME, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'links': {
                'self': url_for('product_area', id=self.id),
            }
        }
        return data


class Feature(SearchableMixin, PaginatedAPIMixin, DAO, db.Model):
    __searchable__ =['title', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(300))
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)
    requests = db.relationship('FeatureRequest', cascade='all, delete, delete-orphan', lazy='dynamic', backref='feature')

    def save(self):
        if not self.is_unique():
            self.title += "_1"
        db.session.add(self)
        db.session.commit()    

    def is_unique(self):
        if self.query.filter_by(title=self.title).count() > 0:
            return False
        return True

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'product_area_id': self.product_area_id,
            'no_requests': self.requests.count(),
            'links': {
                'self': url_for('feature', id=self.id),
                'product_area':url_for('product_area', id=self.product_area_id),
                'requests': url_for('get_feature_request', feature_id=self.id)
            }
        }
        return data


class FeatureRequest(PaginatedAPIMixin, DAO, db.Model):
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime(), default=datetime.utcnow() + timedelta(days=90))

    def to_dict(self):
        data = {
            'feature_id': self.feature_id,
            'client_id': self.client_id,
            'priority': self.priority,
            'target_date': self.target_date,
            'feature_title': self.feature.title,
            'client_name': self.client.name,
            'links': {
                'self': url_for('get_feature_request', feature_id=self.feature_id, client_id=self.client_id),
                'feature': url_for('feature', id=self.feature_id),
                'client': url_for('client', id=self.client_id)
            }
        }
        return data

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)