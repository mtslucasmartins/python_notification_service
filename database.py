from pymongo import MongoClient

client = MongoClient("mongodb://ottimizza:ottimizza@mongodb:27017/")

# gets the database object
db = client.notifications

# gets the collection
subscriptions_collection = db.subscriptions_collection


def find_subscription(username):
    return subscriptions_collection.find_one({
        "username": username
    })


def save_subscription(username, application_id, subscription_info):
    return subscriptions_collection.insert_one({
        "username": username,
        "application_id": application_id,
        "subscription_info": subscription_info
    })
