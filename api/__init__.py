import json
import uuid
import pywebpush as wp

from flask import abort, Blueprint, g, jsonify, render_template, request, Response
from flask_cors import cross_origin

from models import Application, WebPushEndpoint, FCMPushEndpoint, PushNotification
from settings import VAPID

import requests 

# *****************************************************************************
# Blueprint Definition
# *****************************************************************************
notifications_blueprint = Blueprint('notifications', __name__)


# *****************************************************************************
# Error Handling:
# *****************************************************************************
@notifications_blueprint.errorhandler(401)
@cross_origin()
def error_page_unauthorized(e):
    status = 401
    response = json.dumps({"status": "error", "message": "unauthorized"})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)

@notifications_blueprint.errorhandler(404)
@cross_origin()
def error_page_not_found(e):
    status = 404
    response = json.dumps({"status": "error", "message": "not found"})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)


# *****************************************************************************
# Blueprint Endpoints
# *****************************************************************************
@notifications_blueprint.route('/api/v1/applications/register', methods=['POST'])
@cross_origin()
def applications_register():
    # TODO: move this request into an admin_bp.py and restrict access
    application = application.save()

    if application is None:
        return jsonify({'message': 'Could not subsribe!'})

    return jsonify(application.json())

@notifications_blueprint.route('/api/v1/notifications', methods=['GET'])
@cross_origin()
def get_notifications():
    # TODO: ? add order_by and filter values  
    username = request.args.get('username')
    application_id = request.args.get('application_id')

    # getting notification based on arguments passed on query string.
    # TODO: replace username for principal value, accepting request only with access_token
    notifications = PushNotification.find_by_username_and_application_id(username, application_id)
    notifications = list(map(lambda el: el.json(), notifications))


    return jsonify(notifications)
