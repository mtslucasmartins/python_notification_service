
import json
import os
import uuid 

from flask import Blueprint, Flask, request, send_from_directory, send_file
from flask_cors import CORS, cross_origin

from default_settings import STATIC_PATH

apple_notifications = Blueprint('apple_notification', __name__)

from apple_notifications.push_package import PushPackage
from models import APNPushEndpoint


def available_packages():
    return [
        'web.br.com.ottimizza.app'
    ]

def package_exists(package):
    return package in available_packages()


def get_static_path():
    return STATIC_PATH

def get_web_push_package_static_path(web_push_id):
    return 'apple_notifications/{}/pushPackage.zip'.format(web_push_id)


@apple_notifications.route('/<version>/pushPackages/<web_push_id>', methods = ['GET', 'POST'])
@cross_origin()
def request_permission(version, web_push_id):
    """
        Downloading Your Website Package
        GET  > '/<version>/pushPackages/<web_push_id>' -> Downloads.
        POST > '/<version>/pushPackages/<web_push_id>' -> Downloads And Sends Userinfo.

        --
        Validar se webpushid existe.
        Criar JWT para authentication_token
    """
    userinfo = request.get_json()

    if not package_exists(web_push_id):
        return { 'status': 'error' }

    username = userinfo['username']
    application_id = userinfo['application_id']
    authentication_token = str(uuid.uuid4())

    # creating the push package
    push_package = PushPackage(web_push_id)

    # creating the temporary zip...
    zip_file = push_package.create_push_package(authentication_token)
    tmp_file = push_package.create_temporary_zip(zip_file)

    # creating push endpoint on database...
    endpoint = APNPushEndpoint.create(authentication_token, username, application_id, web_push_id)

    return send_file(tmp_file.name, 
                     attachment_filename="pushPackage.zip", 
                     mimetype="application/zip", 
                     as_attachment=True)


@apple_notifications.route('/<version>/devices/<device_token>/registrations/<web_push_id>', methods = ['POST'])
@cross_origin()
def updating_device_permission_policy(version, device_token, web_push_id):
    # 
    authorization_header = request.headers.get('Authorization').strip()
    authentication_token = authorization_header.split(' ')[1].strip()

    endpoint = APNPushEndpoint.find_by_authentication_token(authentication_token)
    endpoint.device_token = device_token
    endpoint.save()

    return json.dumps({ 'status': 'ok'})


@apple_notifications.route('/<version>/devices/<device_token>/registrations/<web_push_id>', methods = ['DELETE'])
@cross_origin()
def forgetting_device_permission_policy(version, device_token, web_push_id):
    print('Version .........: {}'.format(version))
    print('Device Token ....: {}'.format(device_token))
    print('Web Push ID .....: {}'.format(web_push_id))
    print('Authorization ...: {}'.format(request.headers.get('Authorization')))
    return json.dumps({ 'status': 'ok'})


@apple_notifications.route('/<version>/log', methods = ['POST'])
@cross_origin()
def request_permission_error_logs(version):
    try:
        log = request.get_json()
        print("Log: \n" + json.dumps(log, indent=4))
    except Exception as e:
        print(e)
    return json.dumps({})


@apple_notifications.route('/<version>/devices/<device_token>/push/<web_push_id>', methods = ['POST'])
@cross_origin()
def send_notification(version, device_token, web_push_id):
    # Notification Payload
    # payload = request.get_json()
    from apple_notifications.apns.client import APNsClient
    from apple_notifications.apns.payload import Payload, PayloadAlert

    private_key_path = '{}/apple_notifications/{}/apns-prod.pem'.format(STATIC_PATH, web_push_id)

    token_hex = device_token # 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'

    payload_alert = PayloadAlert(
        title="Titulo da Notificacao",
        body="Notificacao Funcionando",
        action="View"
    )

    payload = Payload(
        alert=payload_alert, 
        sound="default", 
        badge=1,
        url_args=["boarding", "A998"]
    )
    topic = web_push_id # 'com.example.App'
    client = APNsClient(private_key_path, password='', use_sandbox=False, use_alternative_port=False)
    client.send_notification(token_hex, payload, topic)
    
    return json.dumps({})


# # To send multiple notifications in a batch
# Notification = collections.namedtuple('Notification', ['token', 'payload'])
# notifications = [Notification(payload=payload, token=token_hex)]
# client.send_notification_batch(notifications=notifications, topic=topic)
