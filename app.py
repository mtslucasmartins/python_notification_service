from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

from database import db
from routes import notification_blueprint
from settings import HOST, PORT, SECRET

application = Flask(__name__)
application.config.from_object('default_settings')

# CORS Filtering
cors = CORS(application)

# database initialization.
db.init_app(application)

@application.before_first_request
def create_tables():
    db.create_all()


@application.route('/api/v1/notifications/apns/push')
def send_js():
    return send_from_directory('static', 'apple_notifications/OttimizzaAngularAppleNotifications.pushPackage')


# Blueprints
application.register_blueprint(notification_blueprint)

#
if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
