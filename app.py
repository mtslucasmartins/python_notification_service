from flask import Flask

from routes import notification_blueprint
from settings import HOST, PORT, SECRET

from database import client

application = Flask(__name__)
application.config['SECRET_KEY'] = SECRET

application.register_blueprint(notification_blueprint)


if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
