
import json

from flask import Blueprint, Flask, request, send_from_directory
from flask_cors import CORS, cross_origin

apple_notification_blueprint = Blueprint('apple_notification', __name__)


def get_web_push_package_static_path(web_push_id):
    return 'apple_notifications/{}/pushPackage.zip'.format(web_push_id)


@apple_notification.route('/<version>/pushPackages/<web_push_id>', methods = ['GET', 'POST'])
@cross_origin()
def request_permission(version, web_push_id):
    """
        Downloading Your Website Package
        GET  > '/<version>/pushPackages/<web_push_id>' -> Downloads.
        POST > '/<version>/pushPackages/<web_push_id>' -> Downloads And Sends Userinfo.
    """
    userinfo = request.get_json()

    filepath = get_web_push_package_static_path(web_push_id)
    filename = "pushPackage.zip"

    return send_from_directory(
        'static', filepath, attachment_filename=filename, mimetype="application/zip", as_attachment=True
    )


@apple_notification.route('/<version>/devices/<device_token>/registrations/<web_push_id>', methods = ['DELETE'])
@cross_origin()
def forgetting_device_permission_policy(version, device_token, web_push_id):
    print('Version .........: {}'.format(version))
    print('Device Token ....: {}'.format(device_token))
    print('Web Push ID .....: {}'.format(web_push_id))
    print('Authorization ...: {}'.format(request.headers.get('Authorization')))
    return json.dumps({ 'status': 'ok'})


@apple_notification.route('/<version>/log', methods = ['POST'])
@cross_origin()
def request_permission_error_logs(version):
    try:
        log = request.get_json()
        print("Log: \n" + json.dumps(log, indent=4))
    except Exception as e:
        print(e)
    return json.dumps({})
