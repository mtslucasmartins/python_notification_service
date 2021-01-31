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
fcm_notifications_blueprint = Blueprint('notification', __name__)

# *****************************************************************************
# Error Handling:
# *****************************************************************************
@notification_blueprint.errorhandler(401)
@cross_origin()
def error_page_unauthorized(e):
    status = 401
    response = json.dumps({"status": "error", "message": "unauthorized"})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)

@notification_blueprint.errorhandler(404)
@cross_origin()
def error_page_not_found(e):
    status = 404
    response = json.dumps({"status": "error", "message": "not found"})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)

# *****************************************************************************
# Blueprint Endpoints
# *****************************************************************************
@notification_blueprint.route('/subscribe', methods=['GET', 'POST'])
@cross_origin()
def fcm_subscribe():
    if request.method == "GET":
        return jsonify({'publicKey': VAPID.get("PUBLIC_KEY")})

    request_body = request.get_json()
    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    registration_id = request_body.get('registrationId')

    subscription = FCMPushEndpoint(username, application_id, registration_id, None)
    subscription = subscription.save()

    if subscription is None:
        return jsonify({'message': 'Could not subsribe!'})

    return jsonify(subscription.json())

@notification_blueprint.route('/<username>/subscriptions', methods=['GET', 'POST'])
@cross_origin()
def fcm_get_subscriptions(username):
    return jsonify(FCMPushEndpoint.get_endpoints_by_username(username))

@notification_blueprint.route('/push', methods=['POST'])
@cross_origin()
def fcm_push():
    request_body = request.get_json()

    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    notification = request_body.get('notification')
    
    # gets the details needed to send the notification    
    application = Application.get_application(application_id)
   
    # store the notification
    notification_model = PushNotification(
        username=username,
        application_id=application_id,
        notification=json.dumps(notification)
    )
    notification_model.save()    

    # sends the notification to all registered endpoints.
    for endpoint in FCMPushEndpoint.get_endpoints_by_username_and_application_id(username, application_id):
        data = { 'notification': notification, 'to': endpoint.get('registration_id') }
        headers = {'Content-Type': 'application/json', 'Authorization': 'key={}'.format(application.get('server_key'))}
        response = requests.post(url='https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
        print(data)
        print(headers)
        print(response.json())

    # extracting data in json format 
    return jsonify({'status': 'success'}) 
