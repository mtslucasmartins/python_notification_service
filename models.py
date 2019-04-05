import json

from database import db

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

    def save(self):
        subscriptions_collection = db.subscriptions_collection
        return subscriptions_collection.insert_one({
            "username": self.__username,
            "application_id": self.application_id,
            "subscription_info": self.__subscription_info
        })

    def update(self, _id):
        subscriptions_collection = db.subscriptions_collection
        subscriptions_collection.update_one({'_id': _id}, {"$set": {
            "username": self.__username,
            "application_id": self.application_id,
            "subscription_info": self.__subscription_info
        }}, upsert=False)
    
