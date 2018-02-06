# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

class TokenMiddleware(BaseAuthentication):
    def authenticate(self, request):
        request.user = None
        #jwt = request.headers.get('authorization', None)
        header_token = request.META['HTTP_AUTHORIZATION']
        jwt = header_token.split(' ')[1]

        if jwt in cache:
            return True
        else:
            raise exceptions.AuthenticationFailed


    def process_exception(self, request, exception):
        if settings.DEBUG :
            intitle = u'{} : {}'.format(exception.__class__.__name__, exception.message)
            print(intitle)
            logging.info(intitle)
        return None


