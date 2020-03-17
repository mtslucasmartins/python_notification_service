import binascii, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_DIR, 'static')

# Application
SECRET_KEY = binascii.hexlify(os.urandom(24))

# Database
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

