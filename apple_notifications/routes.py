
import json
import os
import uuid 

from flask import Blueprint, Flask, request, send_from_directory, send_file
from flask_cors import CORS, cross_origin

from apple_notifications.apns.client import APNsClient, Notification
from apple_notifications.apns.payload import Payload, PayloadAlert
from apple_notifications.push_package import PushPackage

from default_settings import STATIC_PATH

from models import APNPushEndpoint

apple_notifications = Blueprint('apple_notification', __name__)

# listagem de pacotes APNs disponiveis.
def available_packages():
    return [
        'web.br.com.ottimizza.app'
    ]

# método responsavel pela validação de pacote APN.
def package_exists(package):
    return package in available_packages()


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
    endpoint.active = True
    endpoint.save()

    return json.dumps({ 'status': 'ok'})


@apple_notifications.route('/<version>/devices/<device_token>/registrations/<web_push_id>', methods = ['DELETE'])
@cross_origin()
def forgetting_device_permission_policy(version, device_token, web_push_id):
    # 
    authorization_header = request.headers.get('Authorization').strip()
    authentication_token = authorization_header.split(' ')[1].strip()

    endpoint = APNPushEndpoint.find_by_authentication_token(authentication_token)
    endpoint.delete()
    
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
    payload_json = request.get_json()
    
    # building the notification object
    payload_alert = PayloadAlert(**payload_json['alert'])

    payload = Payload(**payload_json)
    payload.alert = payload_alert

    print(json.dumps(payload_alert.dict()))

    print(json.dumps(payload.dict()))

    # certificate location
    private_key_path = '{}/apple_notifications/{}/certificates/apns-pro.pem'.format(STATIC_PATH, web_push_id)

    # creating the connection to APNs and sending notification to device.
    client = APNsClient(private_key_path, password='', use_sandbox=False, use_alternative_port=False)
    client.send_notification(device_token, payload, web_push_id)
    
    return json.dumps({})

@apple_notifications.route('/api/v1/notifications/apns/push', methods = ['POST'])
@cross_origin()
def send_notification_batch():

    request_body = request.get_json()

    username = request_body.get('username')
    application_id = request_body.get('applicationId')
    web_push_id = request_body.get('webPushId')
    notification = request_body.get('notification')

    # building the notification object
    payload_alert = PayloadAlert(**notification['alert'])
    payload = Payload(**notification)
    payload.alert = payload_alert

    # certificate location
    private_key_path = '{}/apple_notifications/{}/certificates/apns-pro.pem'.format(STATIC_PATH, web_push_id)

    notifications: Iterable[Notification] = []
    for endpoint in APNPushEndpoint.get_endpoints_by_username_and_application_id(username, application_id):
        notifications.append(Notification(payload=payload, token=endpoint["device_token"]))

    # creating the connection to APNs and sending notification to device.
    client = APNsClient(private_key_path, password='', use_sandbox=False, use_alternative_port=False)
    client.send_notification_batch(notifications, web_push_id)
    
    return json.dumps({})

# # To send multiple notifications in a batch
# Notification = collections.namedtuple('Notification', ['token', 'payload'])
# notifications = [Notification(payload=payload, token=token_hex)]
# client.send_notification_batch(notifications=notifications, topic=topic)
