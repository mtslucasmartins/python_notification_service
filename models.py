import json

from database import db

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

    

class APNPushEndpoint(db.Model):

    __tablename__ = 'push_apn_endpoints'

    authentication_token = db.Column(db.String(), unique=False, nullable=False, primary_key=True)
    username        = db.Column(db.String(), unique=False, nullable=False, primary_key=True)
    application_id  = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    device_token    = db.Column(db.String(), unique=False, nullable=True, primary_key=True)
    website_push_id = db.Column(db.String(), unique=False, nullable=False, primary_key=True)
    active          = db.Column(db.Boolean)

    def __init(self, authentication_token, username, application_id, website_push_id, device_token=None, active=False):
        self.authentication_token = authentication_token
        self.username        = username
        self.application_id  = application_id
        self.website_push_id = website_push_id
        self.device_token    = device_token
        self.active          = active

    def json(self):
        return {
            "authentication_token": self.authentication_token,
            "username": self.username,
            "application_id": self.application_id,
            "website_push_id": self.website_push_id,
            "device_token": self.device_token,
            "active": self.active
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
    def get_endpoints_by_username_and_application_id(cls, username, application_id):
        endpoints = APNPushEndpoint.query.filter_by(username=username, application_id=application_id).all()
        return list(map(lambda x: x.json(), endpoints))


# class APNPushEndpointBuilder():

#     def __init__(self):
#         self.authentication_token = ''
#         self.application_id = ''
#         self.username = ''
#         self.website_push_id = ''
#         self.device_token = ''
#         self.active = False

#     def authentication_token(self, authentication_token):
#         self.authentication_token = authentication_token
#         return self

#     def application_id(self, application_id):
#         self.application_id = application_id
#         return self

#     def username(self, username):
#         self.username = username
#         return self

#     def website_push_id(self, website_push_id):
#         self.website_push_id = website_push_id
#         return self

#     def device_token(self, device_token):
#         self.device_token = device_token
#         return self

#     def active(self, active):
#         self.active = active
#         return self

#     def build(self, active):
#         self.active = active
#         return self
