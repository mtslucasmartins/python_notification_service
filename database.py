from pymongo import MongoClient
from settings import DATABASE_URI


class MongoDB:

    def __init__(self, uri, db_name="heroku_n7hbh3s5"):
        self.__client = MongoClient(uri)
        self.__db = self.__client[db_name]  # or client.notifications

    def create_collection(self, collection_name="subscriptions_collection"):
        return self.__db[collection_name]  # or db.subscriptions_collection

    def server_info(self):
        self.__client.server_info()

db = MongoDB(DATABASE_URI, "heroku_n7hbh3s5")
