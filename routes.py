
import json
import uuid
import pywebpush as wp

from flask import abort, Blueprint, g, jsonify, render_template, request, Response
from flask_cors import cross_origin

from models import Application, WebPushEndpoint, FCMPushEndpoint, PushNotification
from settings import VAPID

import requests 



notification_blueprint = Blueprint('notification', __name__)

# *****************************************************************************
# Error Handling:
# *****************************************************************************
@notification_blueprint.errorhandler(401)
@cross_origin()
def error_page_unauthorized(e):
    status = 401
    response = json.dumps({"status": "error", "message": "Unauthorized."})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)


@notification_blueprint.errorhandler(404)
@cross_origin()
def error_page_not_found(e):
    status = 404
    response = json.dumps({"status": "error", "message": "Not Found."})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)

# *****************************************************************************
# Requests:
# *****************************************************************************

# @notification_blueprint.route('/api/v1/applications/register', methods=['POST'])
# @cross_origin()
# def applications_register():
#     request_body = request.get_json()
#     application_id = request_body.get('applicationId')
#     server_key = request_body.get('serverKey')

#     application = Application(application_id, server_key)
#     application = application.save()

#     if application is None:
#         return jsonify({'message': 'Could not subsribe!'})

#     return jsonify(application.json())

@notification_blueprint.route('/api/v1/notifications/web/subscribe', methods=['GET', 'POST'])
@cross_origin()
def subscribe():
    if request.method == "GET":
        return jsonify({'publicKey': VAPID.get("PUBLIC_KEY")})

    request_body = request.get_json()
    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    subscription_info = request_body.get('subscriptionInfo')

    subscription = WebPushEndpoint(username, application_id, subscription_info)
    subscription = subscription.save()

    if subscription is None:
        return jsonify({'message': 'Could not subsribe!'})

    return jsonify(subscription.json())

@notification_blueprint.route('/api/v1/notifications/web/unsubscribe', methods=['GET', 'POST'])
@cross_origin()
def unsubscribe():
    return jsonify({'id': ''})

@notification_blueprint.route('/api/v1/notifications/web/<username>/subscriptions', methods=['GET', 'POST'])
@cross_origin()
def get_subscriptions(username):
    return jsonify(WebPushEndpoint.get_endpoints_by_username(username))

@notification_blueprint.route('/api/v1/notifications/web/push', methods=['POST'])
@cross_origin()
def push():
    request_body = request.get_json()

    username = request_body.get('username')
    application_id = request_body.get('applicationId')

    subscription_info = request_body.get('subscriptionInfo')
    notification = {'notification': request_body.get('notification')}

    try:
        wp.webpush(
            subscription_info=subscription_info,
            data=json.dumps(notification),
            vapid_private_key=VAPID.get("PRIVATE_KEY"),
            vapid_claims=VAPID.get("CLAIMS")
        )
    except wp.WebPushException as ex:
        print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
        # Mozilla returns additional information in the body of the response.
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  )
        else:
            print(ex.response)
    except Exception as e:
        print(e)

    return jsonify(notification)

# @notification_blueprint.route('/api/v1/notifications/fcm/subscribe', methods=['GET', 'POST'])
# @cross_origin()
# def fcm_subscribe():
#     if request.method == "GET":
#         return jsonify({'publicKey': VAPID.get("PUBLIC_KEY")})

#     request_body = request.get_json()
#     username = request_body.get('username')
#     application_id = request_body.get('applicationId')
#     registration_id = request_body.get('registrationId')

#     subscription = FCMPushEndpoint(username, application_id, registration_id, None)
#     subscription = subscription.save()

#     if subscription is None:
#         return jsonify({'message': 'Could not subsribe!'})

#     return jsonify(subscription.json())

# @notification_blueprint.route('/api/v1/notifications/fcm/<username>/subscriptions', methods=['GET', 'POST'])
# @cross_origin()
# def fcm_get_subscriptions(username):
#     return jsonify(FCMPushEndpoint.get_endpoints_by_username(username))

# @notification_blueprint.route('/api/v1/notifications/fcm/push', methods=['POST'])
# @cross_origin()
# def fcm_push():
#     request_body = request.get_json()

#     username = request_body.get('username')
#     application_id = request_body.get('applicationId')
#     notification = request_body.get('notification')
    
#     # gets the details needed to send the notification    
#     application = Application.get_application(application_id)
   
#     # store the notification
#     notification_model = PushNotification(
#         username=username,
#         application_id=application_id,
#         notification=json.dumps(notification)
#     )
#     notification_model.save()    

#     # sends the notification to all registered endpoints.
#     for endpoint in FCMPushEndpoint.get_endpoints_by_username_and_application_id(username, application_id):
#         data = { 'notification': notification, 'to': endpoint.get('registration_id') }
#         headers = {'Content-Type': 'application/json', 'Authorization': 'key={}'.format(application.get('server_key'))}
#         response = requests.post(url='https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
#         print(data)
#         print(headers)
#         print(response.json())

#     # extracting data in json format 
#     return jsonify({'status': 'success'}) 

# @notification_blueprint.route('/api/v1/notifications', methods=['GET'])
# @cross_origin()
# def get_notifications():
#     # TODO: ? add order_by and filter values  
#     username = request.args.get('username')
#     application_id = request.args.get('application_id')

#     # getting notification based on arguments passed on query string.
#     # TODO: replace username for principal value, accepting request only with access_token
#     notifications = PushNotification.find_by_username_and_application_id(username, application_id)
#     notifications = list(map(lambda el: el.json(), notifications))


#     return jsonify(notifications)


