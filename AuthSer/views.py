# -*- coding: utf-8 -*-
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserModelSerializer
from .models import User
from .tokens import create_jwt, split_header_token, token_authentication
from .logger_handler import logger
from common.const import const_value, status_code
from .redis import redis_get, redis_set , redis_delete, redis_expire

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
            return Response({'result' : status_code['SIGNUP_SUCCESS'],'registered' : serializer.data},status=status.HTTP_200_OK)
        return Response({'result' : status_code['SIGNUP_INVALID_EMAIL']},status=status.HTTP_200_OK)

    else: #GET - 일단 가입된 모든 사용자 정보 출력
        serializer = UserModelSerializer(User.objects.all(), many=True)
        return Response({'result' : status_code['SUCCESS'], 'registered_user' : serializer.data}, status=status.HTTP_200_OK)
        #return Response({'result' : status_code['SIGNUP_WRONG_PARAMETER']} ,status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
#로그인 - csrf_exempt때문에 FBV로 구현
def login(request):
    if request.method == 'POST':
        try:
            received = json.dumps(request.data)  # 받은 json data 확인을 위함
            logger.debug(received)

            # 사용자가 입력한 이메일 DB에서 확인
            user_id = User.objects.get(user_email=request.data['user_email'])
        except User.DoesNotExist:
            return Response({'result' : status_code['LOGIN_INVALID_EMAIL']}, status=status.HTTP_200_OK)

        print("token_auth_check")
        logger.debug("token_auth_check")

        # Redis에 사용자의 토큰이 있는지 확인 - Session exist의 경우
        if token_authentication(request):
        #if redis_get(split_header_token(request)):
            print(const_value['SESSION_EXIST'])
            logger.debug(const_value['SESSION_EXIST'])
            # 토큰 만료 시간 재설정
            redis_expire(split_header_token(request))

            return Response({'result' : status_code['LOGIN_SUCCESS'],'content' : const_value['SESSION_EXIST'],'User_id': user_id.id} , status=status.HTTP_200_OK)

        # 사용자가 입력한 비밀번호가 DB에 저장된 비밀번호와 같은지 비교 (로그인) - Session이 없는 경우
        else:
            if request.data['password'] == user_id.password:
                # 토큰 생성
                token = create_jwt(user_id)
                # Client 에게 토큰을 json에 담아 보냄
                return Response({'result' : status_code['LOGIN_SUCCESS'], 'Auth_Token' : token, 'User_id' : user_id.id, 'user_name' : user_id.user_name},status=status.HTTP_200_OK)

            else:
                return Response({'result' : status_code['LOGIN_INVALID_PASSWORD']},status=status.HTTP_200_OK)


# json_response 만드는 함수
def json_response(body='',**kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'application/json'
    return Response(**kwargs)


# 로그아웃
class LogoutAPIView(APIView):
    def get(self, request):
        if token_authentication(request): # 토큰이 있는 경우
            token = split_header_token(request)
            logger.debug(token)

            # 레디스에 저장했던 토큰 삭제
            if redis_get(token):
                redis_delete(token)
                return Response({'result' : status_code['LOGOUT_SUCCESS']}, status=status.HTTP_200_OK)

        else: # 토큰이 없는 경우
            return Response({'result' : status_code['LOGOUT_FAILURE'], 'content' : const_value['TOKEN_DOES_NOT_EXIST']}, status=status.HTTP_200_OK)


# 회원 정보 조회 & 수정
#@method_decorator(login_required)
class ProfileAPIView(APIView):
    #회원 정보 조회
    def get(self,request, *args, **kwargs):
        if token_authentication(request):
            try :
                user_id = self.kwargs['user_id']
                print(user_id)
                # 사용자 pk로 현재 user_id 가져옴
                user_info = UserModelSerializer(User.objects.get(id=user_id))
            except User.DoesNotExist:
                return Response({'result' : status_code['USER_INFO_GET_FAILURE']}, status=status.HTTP_200_OK)

            return Response({'result' : status_code['USER_INFO_GET_SUCCESS'], 'User data' : user_info.data}, status=status.HTTP_200_OK)

        else:
            return Response({'result': status_code['USER_INFO_GET_FAILURE'], 'msg': const_value['TOKEN_DOES_NOT_EXIST']},status=status.HTTP_200_OK)

    # 회원 정보 수정
    def post(self, request, *args, **kwargs):
       if token_authentication(request):
            try:
                user_id = self.kwargs['user_id']
                user_info = User.objects.get(id=user_id)
                print("user_id : "+str(user_info.id))
                print("user_email : "+user_info.user_email)
                logger.debug(user_info.user_email)

            except User.DoesNotExist:
                return Response({'result' : status_code['USER_INFO_MODIFY_FAILURE']}, status=status.HTTP_200_OK)

            print("Profile_post_serializer???????")
            serializer = UserModelSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                print("Profile_post_serializer")
                print(serializer.data['user_email'])
                return Response({'result': status_code['USER_INFO_MODIFY_SUCCESS'], 'User data' : serializer.data}, status=status.HTTP_200_OK)
            else:
                print("안들어가마마마마")
                return Response({'result': status_code['USER_INFO_MODIFY_FAILURE'], 'User data': serializer.data},
                            status=status.HTTP_200_OK)

       else:
            return Response({'result': status_code['USER_INFO_MODIFY_FAILURE'], 'content': const_value['TOKEN_DOES_NOT_EXIST']}, status=status.HTTP_200_OK)
