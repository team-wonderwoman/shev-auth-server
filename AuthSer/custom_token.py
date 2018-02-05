# jwt를 만드는 클래스

from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from .serializers import UserModelSerializer


def jwt_reponse_payload_handler(token, user=None, request=None):
    return {
        'token' : token,
        'user' : UserModelSerializer(user, context={'request':request}).data
    }


def jwt_payload_handler(user):
    expiry_date = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA

    return {
        'user_email' : user.user_email,
        'password' : user.password,
        'user_name' : user.user_name,
        'user_tel' : user.user_tel,
        'exp' : expiry_date,
        'orig_iat' : timegm(
            datetime.utcnow().utctimetuple()
        )
    }
