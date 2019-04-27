from flask import Flask
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

# Blueprints
application.register_blueprint(notification_blueprint)


#
if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
