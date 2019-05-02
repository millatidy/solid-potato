from app import db
from app.search import add_to_index, remove_from_index, query_index
from flask import abort, url_for
from datetime import datetime, timedelta


class SessionManager(object):

    """This class subscribes to database events i.e addition,
       updating and deletion of records.

       It then calls methods from class that need to react
       a any of the given events.
    """
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
        PriorityRulesMixin.before_commit(session)

    @classmethod
    def after_commit(cls, session):
        SearchableMixin.after_commit(session)
        session._changes = None


class PriorityRulesMixin(object):

    """This class enforces that no client priority numbers repeat
       for a given client.

       If a collision is detected the reorder_client_priorities()
       method is called to reorder existing feature request for a
       given client.
    """

    @classmethod
    def before_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(
                    obj,
                    PriorityRulesMixin) and cls.client_priority_exits(obj):
                cls.reorder_client_priorities(obj)
        for obj in session._changes['update']:
            if isinstance(
                    obj,
                    PriorityRulesMixin) and cls.client_priority_exits(obj):
                cls.reorder_client_priorities(obj)

    @classmethod
    def reorder_client_priorities(cls, obj):
        features = Feature.query.filter(
            Feature.client_id == obj.client_id,
            Feature.id != obj.id,
            Feature.client_priority >= obj.client_priority).order_by(
            Feature.client_priority.asc()).all()
        current_priority = int(obj.client_priority)
        for feature in features:
            if feature.client_priority == current_priority:
                feature.client_priority += 1
            current_priority += 1

    @classmethod
    def client_priority_exits(cls, obj):
        feature = Feature.query.filter(
            Feature.client_id == obj.client_id,
            Feature.client_priority == obj.client_priority,
            Feature.id != obj.id).first()
        if not feature:
            return False
        return (feature.id != obj.id)


class SearchableMixin(object):

    """This class handles the addition, mutation and deletion of
       a record in ElasticSearch based on database events
       that create, mutate or delete a recored on the Database

       Only models that are sub classes of this class
       can be added to ElasticSearch
    """

    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total['value'] == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj.__tablename__, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class PaginatedAPIMixin(object):

    """This is a utility class that paginates a collection of records
       from the database as per clients request
    """

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


class Client(PaginatedAPIMixin, db.Model):

    """This is the client model.

       Attributes:
          id          primary key an auto incremented integer.
          name        name of client.
          requests    a collection of clients feature requests.

       Methods:
          to_dict()   converts the model from a Client object
                      to a python dictionary.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    requests = db.relationship(
        'Feature',
        cascade='all, delete, delete-orphan',
        lazy='dynamic',
        backref='client')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'no_requests': self.requests.count(),
            'links': {
                'self': url_for(
                    'api.client',
                    id=self.id),
                'requests': url_for(
                    'api.features',
                    client_id=self.id)}}
        return data


class ProductArea(PaginatedAPIMixin, db.Model):

    """This is the Product Area model.

       Attributes:
           id          primary key an auto incremented integer.
           name        name of product area affected that a feature
                       request belongs to.
           features    a collection of feature requests that fall under
                       the given product area.

       Methods:
           to_dict()  converts the model from a ProductArea object
                      to a python dictionary.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    features = db.relationship(
        'Feature',
        cascade='all, delete, delete-orphan',
        lazy='dynamic',
        backref='product_area')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'links': {
                'self': url_for('api.product_area', id=self.id),
            }
        }
        return data


class Feature(
        PriorityRulesMixin,
        SearchableMixin,
        PaginatedAPIMixin,
        db.Model):

    """This is the Feature Request model.

       Attributes:
          id                primary key an auto incremented integer.
          title             a short descriptive name of feature request.
          description       a long description of the feature request.
          client_priority   an integer for the representing the weight of
                            the request for a given client.
          client_id         an interger, foreign key reference to the primary
                            key of the feature request owner(client).
          product_area_id   an interger, foreign key reference to the primary
                            key product area the feature request affects.
          target_date       a date object representing the expected date for
                            the feature request delivery.

       Methods:
          to_dict()     converts the model from a Feature object
                        to a python dictionary.
          from_dict()   converts a python dictionary to a Feature model object
    """

    __searchable__ = ['title', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(300))
    client_priority = db.Column(db.Integer)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id')
    )
    product_area_id = db.Column(
        db.Integer,
        db.ForeignKey('product_area.id'),
        nullable=False)
    target_date = db.Column(
        db.DateTime(),
        default=datetime.utcnow() + timedelta(days=15))

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'productAreaID': self.product_area_id,
            'productArea': self.product_area.name,
            'client': self.client.name,
            'clientID': self.client_id,
            'clientPriority': self.client_priority,
            'targetDate': self.target_date,
            'links': {
                'self': url_for(
                    'api.feature',
                    id=self.id),
                'product_area': url_for(
                    'api.product_area',
                    id=self.product_area_id),
                'client': url_for(
                    'api.client',
                    id=self.client_id)}}
        return data

    def from_dict(self, data):
        if 'target_date' in data:
            if len(data['target_date']) > 0:
                data['target_date'] = datetime.strptime(
                    data['target_date'], '%Y-%m-%d')
            else:
                del data['target_date']
        for field in [
            'title',
            'description',
            'client_id',
            'product_area_id',
            'client_priority',
                'target_date']:
            if field in data:
                setattr(self, field, data[field])

        return self


db.event.listen(db.session, 'before_commit', SessionManager.before_commit)
db.event.listen(db.session, 'after_commit', SessionManager.after_commit)
