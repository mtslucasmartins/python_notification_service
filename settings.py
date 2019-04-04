import binascii
import os
import time

from datetime import datetime, timedelta

# *****************************************************************************
# Application Settings
# 
HOST = "0.0.0.0"
PORT = os.environ.get("PORT", 5000)
SECRET = binascii.hexlify(os.urandom(24))

# *****************************************************************************
# Database Settings
# 
DATABASE_URI = ""
DATABASE_HOST = "mongodb"
DATABASE_PORT = 27017
DATABASE_DATABASE = "notifications"
DATABASE_USERNAME = "ottimizza"
DATABASE_PASSWORD = "ottimizza"

# *****************************************************************************
# Notifications Settings
# 
# added expiration date to 23 hours from now,
# if no expiration is specified, FCM will return a UnregisteredRegistration
# because it forces a date by it's own.
# 
# https://github.com/web-push-libs/pywebpush/issues/79
#
expiration_time = datetime.now() + timedelta(hours=23)
expiration_time = str(round(time.mktime(expiration_time.timetuple())))

VAPID = {
    "CLAIMS": {
        "sub": "mailto:lucas@ottimizza.com.br",
        "exp": expiration_time
    },
    "PUBLIC_KEY": "BLSKBIHrsFCeLUO3FwI95mfSubQiZlno-CTZPDBBoTH6P4CQ-SnEZtlBNM-TWRlk-u3Q36JdjLLk69WYNWJ2rOw",
    "PRIVATE_KEY": "d-FafnJ0zkCN3zH0Vvz9arsvCX15oMk8WmyJyBjWFM0"
}
