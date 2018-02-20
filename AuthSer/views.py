# -*- coding: utf-8 -*-
import json, requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserModelSerializer
from .models import User
from .create_token import create_jwt
from .split_token import split_header_token
from .logger_handler import logger
from common.const import const_value, status_code
from chat.models import GroupMember,TopicMember, ChatRoomMember

# from rest_framework import generics
# from django.contrib.auth.models import User
# from .serializers import OauthSerializer

#
# class OAuthUserAPIView(APIView):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer

# Create your views here.
# 회원가입 - csrf_exempt 때문에 FBV로 구현
@api_view(['GET','POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        received = json.dumps(request.data) #받은 json data 확인을 위함
        logger.debug(received)

        #Model에 저장 위해 직렬화
        serializer = UserModelSerializer(data=request.data)

        if serializer.is_valid():
            # TODO 비밀번호 암호화  - 함수로 구현하기
            serializer.save()
            # 회원 가입 확인 메일 발송
            #send_registration_mail(serializer)
            status_code['SIGNUP_SUCCESS']['data'] = serializer.data
            return Response({'result' : status_code['SIGNUP_SUCCESS']},status=status.HTTP_200_OK)
        return Response({'result' : status_code['SIGNUP_INVALID_EMAIL']},status=status.HTTP_200_OK)

    else: #GET - 일단 가입된 모든 사용자 정보 출력
        serializer = UserModelSerializer(User.objects.all(), many=True)
        status_code['SIGNUP_SUCCESS']['data'] = serializer.data
        return Response({'result' : status_code['SIGNUP_SUCCESS']}, status=status.HTTP_200_OK)
        #return Response({'result' : status_code['SIGNUP_WRONG_PARAMETER']} ,status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
#로그인 - csrf_exempt때문에 FBV로 구현
def login(request):
    if request.method == 'POST': # POST의 경우
        try:
            received = json.dumps(request.data)  # 받은 json data 확인을 위함
            logger.debug(received)

            # 사용자가 입력한 이메일 DB에서 확인
            user_query = User.objects.get(user_email=request.data['user_email'])

        except User.DoesNotExist:
            return Response({'result' : status_code['LOGIN_INVALID_EMAIL']}, status=status.HTTP_200_OK)


        # redis_set("yejin","choi")
        print("token_auth_check")
        logger.debug("token_auth_check")

        # Redis에 사용자의 토큰이 있는지 확인 - Session exist의 경우
        # if token_authentication(request):
        # #if redis_get(split_header_token(request)):
        #     print(const_value['SESSION_EXIST'])
        #     logger.debug(const_value['SESSION_EXIST'])
        #     # 토큰 만료 시간 재설정
        #     redis_expire(split_header_token(request))
        #
        #     status_code['LOGIN_SUCCESS']['data'] = {'User_id' : user_id.id , 'addtional' : const_value['SESSION_EXIST']}
        #     return Response({'result' : status_code['LOGIN_SUCCESS']} , status=status.HTTP_200_OK)



        # # 사용자가 입력한 비밀번호가 DB에 저장된 비밀번호와 같은지 비교 (로그인) - Session이 없는 경우
        # else:
        if request.data['password'] == user_query.password: # 로그인 성공

            # 토큰 생성
            token = create_jwt(user_query)

            status_code['LOGIN_SUCCESS']['data'] = {'Token' : token, 'User_id' : user_query.id, 'user_name' :user_query.user_name }
            # Client 에게 토큰을 json에 담아 보냄

            print(user_query)
            send_data = {'Token' : token, 'User' : user_query}

            r = requests.post("http://192.168.0.24:8001/session/create/", data=send_data)
            print("새로운 request")

            # print(r.json())
            # print(dir(r.json()))
            # print(r.json().get('result'))

            if r.json().get('result').get('code') == 1 :
                return Response({'result' : status_code['LOGIN_SUCCESS']}, status=status.HTTP_200_OK)

        else:
            return Response({'result' : status_code['LOGIN_INVALID_PASSWORD']},status=status.HTTP_200_OK)
#
# @csrf_exempt
# def oauth_login(request):
#     if request.method == 'GET':
#         print("OAUTH GET")
#         user = request.user
#         try:
#             google_login = user.social_auth.get(provider='google')
#         except UserSocialAuth.DoesNotExist:
#             google_login = None
#
#         return Response({'result' : status_code['SUCCESS']}, status=status.HTTP_200_OK)
#
#     else:
#         print("OAUTH PRINT")
#         user = request.user
#         try:
#             google_login = user.social_auth.get(provider='google')
#         except UserSocialAuth.DoesNotExist:
#             google_login = None
#
#         return Response({'result': status_code['SUCCESS']}, status=status.HTTP_200_OK)

# TODO OAuth
# class UserList(generics.ListAPIView):
#   queryset = User.objects.all()
#   serializer_class = OauthSerializer


# TODO OAuth
# class CurrentUser(generics.RetrieveAPIView):
#   def get(self, request):
#       serializer = OauthSerializer(request.user)
#       return Response(serializer.data)

# 로그아웃
class LogoutAPIView(APIView):
    def get(self, request):
        token = split_header_token(request)
        if token is None :
            status_code['LOGOUT_FAIL']['data'] = const_value['HEADER_DOES_NOT_EXIST']
            return Response({'result' : status_code['LOGOUT_FAIL']}, status=status.HTTP_200_OK)

        else:
            send_data = {'Token': token}

            r = requests.post("http://192.168.0.24:8001/session/check/",data=send_data)
            print("새로운 request")

            print(r.json())

            if r.json().get('result').get('code') == 1 : # 세션이 있는 경우

                rq = requests.post("http://192.168.0.24:8001/session/destroy/", data=send_data)
                print("새로운 request")

                return Response({'result': status_code['LOGOUT_SUCCESS']}, status=status.HTTP_200_OK)
        #
        # if token_authentication(request): # 토큰이 있는 경우
        #     token = split_header_token(request)
        #     logger.debug(token)

            # # 레디스에 저장했던 토큰 삭제
            # if redis_get(token):
            #     redis_delete(token)
            #     return Response({'result' : status_code['LOGOUT_SUCCESS']}, status=status.HTTP_200_OK)

            else: # 세션이 없는 경우
                status_code['LOGOUT_FAIL']['data'] =  const_value['TOKEN_DOES_NOT_EXIST']
                return Response({'result' : status_code['LOGOUT_FAIL']}, status=status.HTTP_200_OK)


# 회원 정보 조회 & 수정
#@method_decorator(login_required)
class ProfileAPIView(APIView):
    # [GET] 회원 정보 조회
    def get(self,request, *args, **kwargs):
        # token = split_header_token(request)
        # if token is None:
        #     status_code['LOGOUT_FAIL']['data'] = const_value['HEADER_DOES_NOT_EXIST']
        #     return Response({'result': status_code['LOGOUT_FAIL']}, status=status.HTTP_200_OK)
        #
        # else:
        #     send_data = {'Token': token}
        #
        #     r = requests.post("http://192.168.0.24:8001/session/check/", data=send_data)
        #     print("새로운 request")
        #
        #     print(r.json())
        #
        #     if r.json().get('result').get('code') == 1:  # 세션이 있는 경우
        try :
            user_id = self.kwargs['user_id']
            print(user_id)
            # 사용자 pk로 현재 user_id 가져옴
            user_info = UserModelSerializer(User.objects.get(id=user_id))
        except User.DoesNotExist:
            return Response({'result' : status_code['USER_INFO_GET_FAIL']}, status=status.HTTP_200_OK)

        status_code['USER_INFO_GET_SUCCESS']['data'] = user_info.data
        return Response({'result' : status_code['USER_INFO_GET_SUCCESS']}, status=status.HTTP_200_OK)

            # else:
            #     status_code['USER_INFO_GET_FAIL']['data'] = const_value['TOKEN_DOES_NOT_EXIST']
            #     return Response({'result': status_code['USER_INFO_GET_FAIL']},status=status.HTTP_200_OK)

    # [PUT] 회원 정보 수정
    def put(self, request, *args, **kwargs):
        # token = split_header_token(request)
        # if token is None:
        #     status_code['LOGOUT_FAIL']['data'] = const_value['HEADER_DOES_NOT_EXIST']
        #     return Response({'result': status_code['LOGOUT_FAIL']}, status=status.HTTP_200_OK)
        #
        # else:
        #     send_data = {'Token': token}
        #
        #     r = requests.post("http://192.168.0.24:8001/session/check/", data=send_data)
        #     print("새로운 request")
        #
        #     print(r.json())
        #
        #     if r.json().get('result').get('code') == 1:  # 세션이 있는 경우
        try:
            user_id = self.kwargs['user_id'] # 사용자의 user_id 가져옴
            user_info = User.objects.get(pk=user_id) # 사용자의 회원 정보를 담고 있는 User object를 가져옴
            print("user_id : "+str(user_info.id))
            print("user_email : "+user_info.user_email)
            logger.debug(user_info.user_email)

        except User.DoesNotExist:
            return Response({'result' : status_code['USER_INFO_MODIFY_FAIL']}, status=status.HTTP_200_OK)

        print("Profile_post_serializer???????")
        print(request.data)

        serializer = UserModelSerializer(user_info, data=request.data, partial=True) # 정보 update

        if serializer.is_valid():
            serializer.save()
            status_code['USER_INFO_MODIFY_SUCCESS']['data'] = serializer.data
            return Response({'result': status_code['USER_INFO_MODIFY_SUCCESS']}, status=status.HTTP_200_OK)
        else:
            status_code['USER_INFO_MODIFY_FAIL']['data'] = serializer.errors
            return Response({'result': status_code['USER_INFO_MODIFY_FAIL']},
                        status=status.HTTP_200_OK)

            # else:
            #     status_code['USER_INFO_MODIFY_FAIL']['data'] = const_value['TOKEN_DOES_NOT_EXIST']
            #     return Response({'result': status_code['USER_INFO_MODIFY_FAIL']}, status=status.HTTP_200_OK)


# 회원 탈퇴
class SignoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # token = split_header_token(request)
        # if token is None:
        #     status_code['LOGOUT_FAIL']['data'] = const_value['HEADER_DOES_NOT_EXIST']
        #     return Response({'result': status_code['LOGOUT_FAIL']}, status=status.HTTP_200_OK)
        #
        # else:
        #     send_data = {'Token': token}
        #
        #     r = requests.post("http://192.168.0.24:8001/session/check/", data=send_data)
        #     print("새로운 request")
        #
        #     print(r.json())
        #
        #     if r.json().get('result').get('code') == 1:  # 세션이 있는 경우
        try:
            token = split_header_token(request)
            user_id = self.kwargs['user_id'] # 사용자의 user_id를 가져옴
            print(user_id)


            print("sssss")
            #
            # topic = TopicMember.objects.filter(user_id=user_id)
            # print(topic)
            # if topic is not None:
            #     topic.delete()
            #
            # chat = ChatRoomMember.objects.filter(user=user_id)
            # if chat is not None:
            #     chat.delete()
            #
            # group = GroupMember.objects.filter(user_id=user_id)
            # if group is not None:
            #     group.delete()

            user_query = User.objects.get(pk=user_id) # 사용자의 회원 정보를 담고 있는 User object를 가져옴
            print(user_query)
            user_query.delete()
            print("delete완료")

            send_data = {'Token' : token}

            rq = requests.post("http://192.168.0.24:8001/session/destroy/", data=send_data)

            print("새로운 request")

            return Response({'result' : status_code['USER_SIGNOUT_SUCCESS']}, status=status.HTTP_200_OK)

        except:
            status_code['USER_SIGNOUT_FAIL']['data'] = "Can't delete user objects"
            return Response({'result' : status_code['USER_SIGNOUT_FAIL']}, status=status.HTTP_200_OK)

            # else:
            #     status_code['USER_SIGNOUT_FAIL']['data'] = const_value['TOKEN_DOES_NOT_EXIST']
            #     return Response({'result': status_code['USER_SIGNOUT_FAIL']}, status=status.HTTP_200_OK)



