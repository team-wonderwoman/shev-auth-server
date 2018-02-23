# -*- coding: utf-8 -*-
import requests

from rest_framework import exceptions, status
from rest_framework.response import Response
from common.const import const_value, status_code
from .split_token import split_header_token
from django.http import JsonResponse

class TokenMiddleware(object):
    def __init__(self, get_response=None):
        print("init")
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = ['192.168.0.24', '0.0.0.0']
        ip = request.META.get('REMOTE_ADDR')

        print(request.path)

        #print(request.path)

        if request.path.startswith('/api/accounts/signup/') \
                or request.path.startswith('/api/accounts/login/') \
                or request.path.startswith('/api/accounts/logout/')\
                or request.path.startswith('/admin/') \
                or request.path.startswith('/oauth/google/'):

            response = self.get_response(request)
            return response

        else:
            token = split_header_token(request)


            if token is None:
                status_code['FAIL']['data'] = const_value['HEADER_DOES_NOT_EXIST']
                return JsonResponse({'result': status_code['FAIL']}, status=status.HTTP_200_OK)

            else: # 헤더에 토큰 있어
                send_data = {'Token': token}

                r = requests.post("http://192.168.0.24:8001/session/check/", data=send_data)

                if r.json().get('result').get('code') == 1:  # 세션이 있는 경우
                    response = self.get_response(request)
                    return response


                else:
                    status_code['FAIL']['data'] = const_value['SESSION_DOES_NOT_EXIST']
                    return JsonResponse({'result': status_code['FAIL']}, status=status.HTTP_200_OK)
