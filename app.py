from settings import DATABASE_URI, HOST, PORT, SECRET

from flask import Flask
from database import MongoDB
from routes import notification_blueprint


application = Flask(__name__)
application.config['SECRET_KEY'] = SECRET

application.register_blueprint(notification_blueprint)


if __name__ == "__main__":
    application.run(host=HOST, port=PORT, debug=True)
