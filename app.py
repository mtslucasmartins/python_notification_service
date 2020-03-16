from flask import Flask, request, send_from_directory
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


# webServiceURL/version/pushPackages/websitePushID

@application.route('/v2/pushPackages/web.com.herokuapp.angular-apple-notifications', methods = ['POST'])
def request_permission():
    print(request.get_json())
    return send_from_directory('static', 'apple_notifications/OttimizzaAngularAppleNotifications.pushPackage.zip')


# Blueprints
application.register_blueprint(notification_blueprint)

#
if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
