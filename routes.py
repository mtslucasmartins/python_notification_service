
import json
import pywebpush as wp

from flask import abort, Blueprint, g, jsonify, render_template, request, Response

from models import Subscription
from settings import VAPID

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
@notification_blueprint.route('/api/v1/notifications/subscribe', methods=['GET', 'POST'])
def subscribe():
    # GET Request
    if request.method == "GET":
        return jsonify({'publicKey': VAPID.get("PUBLIC_KEY")})

    # POST Request
    request_body = request.get_json()

    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    subscription_info = request_body.get('subscriptionInfo')

    # saves subscriptions to database
    subscription = Subscription(username, application_id, subscription_info)
    subscription = subscription.save()

    # generates an id for reference.
    webpush_key = str(uuid.uuid4())

    return jsonify({'id': webpush_key})


@notification_blueprint.route('/api/v1/notifications/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    return jsonify({'id': ''})


@notification_blueprint.route('/api/v1/notifications/push', methods=['POST'])
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
