import hmac
import hashlib
import base64
import json 
import datetime

import jwt

from settings import JWT_PUBLIC_KEY


class InvalidJWTSignatureException(Exception):
    pass


class InvalidJWTPublicKeyException(Exception):
    pass


def jwt_verify_and_decode(access_token, public_key=JWT_PUBLIC_KEY):
    """Method for validating and decoding the JWT access token."""

    decoded_jwt = {}
    algorithms = "RS256"
    options = { "verify_signature": True }

    try:
        print(access_token)
        print(public_key)
        decoded_jwt = jwt.decode(
            access_token, key=public_key, algorithms=algorithms, options=options
        )

        return decoded_jwt
    except Exception as e:
        raise InvalidJWTSignatureException('Invalid signature or jwt token')

    return decoded_jwt
