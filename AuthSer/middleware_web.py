# -*- coding: utf-8 -*-
import logging, datetime,json
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework import exceptions, status
from rest_framework.response import Response
from common.const import const_value, status_code
from AuthSer.tokens import token_authentication, split_header_token
from AuthSer.redis import redis_get
from AuthSer.logger_handler import logger


class TokenMiddleware(object):
    def __init__(self, request):
        pass

    def __call__(self,request):

        header = request.META.get('HTTP_AUTHORIZATION', None)

        print("여기!!!!")
        print(header)
        logger.debug(header)

        if token_authentication(request):
            print("token 이 있어")
            logger.debug("token 이 있어")
            return
        else:
            print("token이없어")
            json_msg = json.dumps({'result': status_code['LOGOUT_FAILURE'], 'msg': const_value['TOKEN_DOES_NOT_EXIST']})
            return HttpResponse(json_msg,status=status.HTTP_200_OK)

        response = self.get_reponse(request)

        return response

        #if token_authentication():
         #   return
        #else:
         #   return HttpResponse({'result': status_code['LOGOUT_FAILURE'], 'msg': const_value['TOKEN_DOES_NOT_EXIST']},
          #                      status=status.HTTP_200_OK)