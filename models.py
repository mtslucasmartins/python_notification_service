import json

from database import db
from bson.json_util import dumps

class SubscriptionService:

    def __init__(self):
        pass

    @staticmethod
    def find_by_username(username):
        subscriptions_collection = db.create_collection('subscriptions_collection')
        return json.loads(dumps(subscriptions_collection.find({
            "username": username
        })))


class Subscription:

    def __init__(self, username, application_id, subscription_info):
        self.__username = username
        self.__application_id = application_id
        self.__subscription_info = subscription_info

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def application_id(self):
        return self.__application_id

    @application_id.setter
    def application_id(self, application_id):
        self.__application_id = application_id

    @property
    def subscription_info(self):
        return self.__subscription_info
        
    @subscription_info.setter
    def subscription_info(self, subscription_info):
        self.__subscription_info = subscription_info 

    def document(self):
        return {
            "username": self.__username,
            "application_id": self.application_id,
            "subscription_info": self.__subscription_info
        }

    def save(self):
        subscriptions_collection = db.create_collection('subscriptions_collection')
        return subscriptions_collection.update(self.document(), {"$set": self.document()}, upsert=True)
