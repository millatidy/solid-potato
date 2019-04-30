from app import db
from app.search import add_to_index, remove_from_index, query_index
from flask import abort, url_for
from datetime import datetime, timedelta


class SessionManager(object):

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

    @classmethod
    def before_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, PriorityRulesMixin):
                if int(obj.client_priority.priority) == 1:
                    cls.suspend_request_orders(obj)
        for obj in session._changes['update']:
            if isinstance(obj, PriorityRulesMixin):
                if int(obj.client_priority.priority) == 1:
                    cls.suspend_request_orders(obj.client_id)

    @classmethod
    def suspend_request_orders(cls, obj):
        Feature.query.filter(ClientPriority.priority > 1, Feature.client_id==obj.client_id, Feature.id!=obj.id).update(dict(suspended=True), synchronize_session=False)
        obj.suspended=False


class SearchableMixin(object):

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

    # @classmethod
    # def before_commit(cls, session):
    #     session._changes = {
    #         'add': list(session.new),
    #         'update': list(session.dirty),
    #         'delete': list(session.deleted)
    #     }

    @classmethod
    def after_commit(cls, session):
        print(session._changes)
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


class Feature(PriorityRulesMixin, SearchableMixin, PaginatedAPIMixin, db.Model):

    __searchable__ = ['title', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(db.String(300))
    suspended = db.Column(db.Boolean, default=False)
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
        default=datetime.utcnow() + timedelta(days=90))
    client_priority = db.relationship(
        'ClientPriority',
        cascade='all, delete, delete-orphan',
        backref='feature', uselist=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'productAreaID': self.product_area_id,
            'productArea': self.product_area.name,
            'client': self.client.name,
            'clientID': self.client_id,
            'clientPriority': self.client_priority.priority,
            'targetDate': self.target_date,
            'suspended': self.suspended,
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

    # needs modification unique contraint violation
    def validate(self):
        priority = ClientPriority.query.filter_by(
            priority=self.client_priority.priority,
            client_id=self.client_id).first()
        if priority:
            if self.id == priority.feature_id:
                return True
            return False
        return True

    def convert_date(self, string_date):
        date_arr = string_date.split("-")
        py_date = datetime(int(date_arr[0]), int(
            date_arr[1]), int(date_arr[2]))
        return py_date

    def from_dict(self, data):
        data['target_date'] = self.convert_date(
            data['target_date']) if 'target_date' in data else None
        cli_pr = ClientPriority()
        cli_pr.client_id = data['client_id']
        cli_pr.priority = data['client_priority']
        for field in [
            'title',
            'description',
            'client_id',
            'product_area_id',
                'target_date']:
            if field in data:
                setattr(self, field, data[field])

        setattr(self, "client_priority", cli_pr)

        return self


class ClientPriority(db.Model):

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id'),
        primary_key=True)
    priority = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'))


db.event.listen(db.session, 'before_commit', SessionManager.before_commit)
db.event.listen(db.session, 'after_commit', SessionManager.after_commit)
