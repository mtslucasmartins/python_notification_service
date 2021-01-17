import json
import uuid

from datetime import datetime
from database import db
from sqlalchemy.dialects.postgresql import UUID

class Application(db.Model):
    __tablename__ = 'applications'


    application_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    server_key = db.Column(db.String(), unique=False, nullable=False)

    def __init__(self, application_id, server_key):
        self.application_id = application_id
        self.server_key = server_key

    def json(self):
        return {
            "application_id": self.application_id,
            "server_key": self.server_key
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return None
        return self

    @classmethod
    def get_application(cls, application_id):
        return Application.query.filter_by(application_id = application_id).first().json()


class WebPushEndpoint(db.Model):
    __tablename__ = 'push_web_endpoints'

    username = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    application_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    subscription_info = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)

    def __init__(self, username, application_id, subscription_info):
        self.username = username
        self.application_id = application_id
        self.subscription_info = json.dumps(subscription_info)

    def json(self):
        return {
            "username": self.username,
            "application_id": self.application_id,
            "subscription_info": json.loads(self.subscription_info)
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return None
        return self

    @classmethod
    def get_endpoints_by_username(cls, username):
        endpoints = WebPushEndpoint.query.filter_by(username = username).all()
        return { 'endpoints': list(map(lambda x: x.json(), endpoints)) }
    

class FCMPushEndpoint(db.Model):
    __tablename__ = 'push_fcm_endpoints'

    username = db.Column(db.String(), unique=False, nullable=False, primary_key=True)
    application_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    registration_id = db.Column(db.String(), unique=False, nullable=False, primary_key=True)
    server_key = db.Column(db.String(), unique=False, nullable=True)

    def __init__(self, username, application_id, registration_id, server_key):
        self.username = username
        self.application_id = application_id
        self.registration_id = registration_id
        self.server_key = server_key

    def json(self):
        return {
            "username": self.username,
            "application_id": self.application_id,
            "registration_id": self.registration_id,
            "server_key": self.server_key
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return None
        return self

    @classmethod
    def get_endpoints_by_username(cls, username):
        endpoints = FCMPushEndpoint.query.filter_by(username = username).all()
        # { 'endpoints': list(map(lambda x: x.json(), endpoints)) }
        return list(map(lambda x: x.json(), endpoints))

    @classmethod
    def get_endpoints_by_username_and_application_id(cls, username, application_id):
        endpoints = FCMPushEndpoint.query\
                        .filter_by(username = username, application_id = application_id).all()
        return list(map(lambda x: x.json(), endpoints))


class PushNotification(db.Model):
    """"""
    __tablename__ = 'notifications'

    id             = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)

    username       = db.Column(db.String(), nullable=False)
    application_id = db.Column(db.String(), nullable=False)

    notification   = db.Column(db.String(), nullable=False)

    is_seen        = db.Column(db.Boolean(), nullable=False, default=False)

    created_at     = db.Column(db.Date())
    updated_at     = db.Column(db.Date())

    def __repr__(self):
        return str(json.dumps(self.json()))
    
    def json(self):
        return { 
            "id": self.id,
            "username": self.username, 
            "application_id": self.application_id,
            "notification": json.loads(self.notification),
            "is_seen": self.is_seen,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def pre_persist(self):
        if self.created_at == None:
                self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        try:
            self.pre_persist()

            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise Exception('Erro ao inserir notificação!')

    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls) \
                         .filter(cls.username == username).all()

    @classmethod
    def find_by_username_and_application_id(cls, username, application_id=None):
        if application_id == None:
            return cls.find_by_username(username)

        return db.session.query(cls) \
                         .filter(cls.username == username) \
                         .filter(cls.application_id == application_id).all()
