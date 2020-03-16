from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS, cross_origin

from database import db
from routes import notification_blueprint
from settings import HOST, PORT, SECRET

import json

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

@application.route('/<version>/pushPackages/web.com.herokuapp.angular-apple-notifications', methods = ['GET', 'POST'])
def request_permission(version):
    print(request.get_json())

    filepath = 'apple_notifications/OttimizzaAngularAppleNotifications.pushPackage.zip'
    filename = "OttimizzaAngularAppleNotifications.pushPackage.zip"
    mimetype = "application/zip"

    # return Response(xml, mimetype='application/zip')
    return send_from_directory('static', filepath, attachment_filename=filename, mimetype=mimetype)


@application.route('/<version>/log', methods = ['POST'])
def request_permission_error_logs(version):
    try:
        print("Log: \n" + json.dumps(request.get_json(), indent=4))
    except Exception as e:
        print(e)

    return json.dumps({})


# Blueprints
application.register_blueprint(notification_blueprint)

#
if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
