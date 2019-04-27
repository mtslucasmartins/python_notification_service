
import json
import uuid
import pywebpush as wp

from flask import abort, Blueprint, g, jsonify, render_template, request, Response

from models import Application, WebPushEndpoint, FCMPushEndpoint
from settings import VAPID

import requests 



notification_blueprint = Blueprint('notification', __name__)

# *****************************************************************************
# Error Handling:
# *****************************************************************************
@notification_blueprint.errorhandler(401)
def error_page_unauthorized(e):
    status = 401
    response = json.dumps({"status": "error", "message": "Unauthorized."})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)


@notification_blueprint.errorhandler(404)
def error_page_not_found(e):
    status = 404
    response = json.dumps({"status": "error", "message": "Not Found."})
    headers = {"Content-Type": "application/json"}
    return (response, status, headers)

# *****************************************************************************
# Requests:
# *****************************************************************************
@notification_blueprint.route('/api/v1/notifications/web/subscribe', methods=['GET', 'POST'])
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
def unsubscribe():
    return jsonify({'id': ''})


@notification_blueprint.route('/api/v1/notifications/web/<username>/subscriptions', methods=['GET', 'POST'])
def get_subscriptions(username):
    return jsonify(WebPushEndpoint.get_endpoints_by_username(username))



@notification_blueprint.route('/api/v1/notifications/web/push', methods=['POST'])
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

@notification_blueprint.route('/api/v1/applications/register', methods=['POST'])
def applications_register():
    request_body = request.get_json()
    application_id = request_body.get('applicationId')
    server_key = request_body.get('serverKey')

    application = Application(application_id, server_key)
    application = application.save()

    if application is None:
        return jsonify({'message': 'Could not subsribe!'})

    return jsonify(application.json())

@notification_blueprint.route('/api/v1/notifications/fcm/subscribe', methods=['GET', 'POST'])
def fcm_subscribe():
    if request.method == "GET":
        return jsonify({'publicKey': VAPID.get("PUBLIC_KEY")})

    request_body = request.get_json()
    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    registration_id = request_body.get('registrationId')

    server_key = 'AAAASjkIBhE:APA91bGe34jxD7a_Pd08ZsynOXz-6vaIPdAtqZ31atgLfvqXedeAw0r7VYAHtLPwFY8hxyssVRRxGbVAnoitf00VglU2ck5cjjFwE4IZoRs5xNQgKZLPksTKyFpubnI8wsgtJ5hoFNs2'
    
    subscription = FCMPushEndpoint(username, application_id, registration_id, server_key)
    subscription = subscription.save()

    if subscription is None:
        return jsonify({'message': 'Could not subsribe!'})

    return jsonify(subscription.json())

@notification_blueprint.route('/api/v1/notifications/fcm/<username>/subscriptions', methods=['GET', 'POST'])
def fcm_get_subscriptions(username):
    return jsonify(FCMPushEndpoint.get_endpoints_by_username(username))


@notification_blueprint.route('/api/v1/notifications/fcm/push', methods=['POST'])
def fcm_push():
    request_body = request.get_json()

    # Request Body
    # busca endpoints 
    # registration_id = 'ce_413wDclk:APA91bEVE0jpCE3Gqps53iiP4glm_Bk_2GeZvOj-jkt6Ed1kTImQSr1DJnn5KHWWBkSgPz318pCE5vSI5lT-9j-ugpPfQ8WyRCHjrOK33F6u3XVMxdbn4VdjkLhLrUDBrplyJaja22Sr';
    # server_key = 'AAAASjkIBhE:APA91bGe34jxD7a_Pd08ZsynOXz-6vaIPdAtqZ31atgLfvqXedeAw0r7VYAHtLPwFY8hxyssVRRxGbVAnoitf00VglU2ck5cjjFwE4IZoRs5xNQgKZLPksTKyFpubnI8wsgtJ5hoFNs2'
    
    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    server_key = request_body.get('serverKey')
    notification = request_body.get('notification')
    
    application = Application.get_application(request_body.get('applicationId'))

    for endpoint in FCMPushEndpoint.get_endpoints_by_username_and_application_id(username, application_id):
        data = { 'notification': notification, 'to': endpoint.get('registration_id') }
        headers = {'Content-Type': 'application/json', 'Authorization': 'key={}'.format(application.get('server_key'))}
        response = requests.post(url='https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
        print(data)
        print(headers)
        print(response.json())

    # extracting data in json format 
    return jsonify({'status': 'success'}) 


