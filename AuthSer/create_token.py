# -*- coding: utf-8 -*-
import jwt, datetime
from common.const import const_value
from .logger_handler import logger
# 토큰 관련 클래스 - 토큰 생성, 헤더에 담긴 토큰 가져오기

# 토큰 생성 함
def create_jwt(query):

    payload = {
        'user_email': query.user_email,
        'user_name': query.user_name,
        'password': query.password,
        'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    created_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
    token = {'token': created_token}

    print(created_token.decode('utf-8'))

    return created_token
