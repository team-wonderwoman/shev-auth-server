# -*- coding: utf-8 -*-

import json,jwt,datetime,logging
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserModelSerializer
from .models import User


# Create your views here.
# 회원가입 - csrf_exempt 때문에 FBV로 구현
@api_view(['GET','POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        received = json.dumps(request.data) #받은 json data 확인을 위함
        logging.info(received)

        #Model에 저장 위해 직렬화
        serializer = UserModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'received_SignUp_Success':request.data},status=status.HTTP_200_OK)
        return Response({'result_message':'Email Already exists'},status=status.HTTP_200_OK)

    else: #GET - 일단 가입된 모든 사용자 정보 출력
        serializer = UserModelSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
#로그인 - csrf_exempt때문에 FBV로 구현
def login(request):
    if request.method == 'POST':
        try:
            received = json.dumps(request.data)  # 받은 json data 확인을 위함
            logging.info(received)

            # 사용자가 입력한 이메일 확인
            user_id = UserModelSerializer(User.objects.get(user_email=request.data['user_email']))
        except user_id.DoesNotExist:
            return Response({'result_message' : 'Your Email Does Not Exists'}, status=status.HTTP_200_OK)


        # 사용자가 입력한 비밀번호가 DB에 저장된 비밀번호와 같은지 비교
        if request.data['password'] == user_id.data['password']:
            # 토큰 생성

            #token = create_jwt(user_id)

            payload = {
                'user_email' : user_id.data['user_email'],
                'user_name' : user_id.data['user_name'],
                'password' : user_id.data['password'],
                'datetime' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            created_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')

            token = {'token' : created_token }

            logging.info('Created_token : ')
            logging.info(token)

            # 레디스에 토큰 저장
            cache.set(created_token.decode('utf-8'), user_id.data['user_email'], timeout=5000)

            # Client 에게 토큰을 json에 담아 보냄
            return Response({'Login_Success' : token},status=status.HTTP_200_OK)
        else:
            return Response({'result_message' : 'Invalid Password. Please Check your password.'},status=status.HTTP_200_OK)


# json_response 만드는 함수
def json_response(body='',**kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'application/json'
    return Response(**kwargs)

# 토큰 생성
def create_jwt(self, *args, **kwargs):
    payload = {
        'user_email': kwargs.data['user_email'],
        'user_name': kwargs.data['user_name'],
        'password': kwargs.data['password'],
        'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    created_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
    token = {'token': created_token}

    # 레디스에 토큰 저장
    cache.set(created_token.decode('utf-8'), kwargs.data['user_email'])

    return {'token' : created_token}

# 헤더에 담긴 토큰 가져오기
def split_header_token(request):
    header_token = request.META['HTTP_AUTHORIZATION']
    token = header_token.split(' ')[1]

    return token

# 토큰 검사 (인증) - 인증된 사용자는 True, 아니면 False
def token_authentication(request):
    # 헤더에 담긴 토큰 레디스에 있는지 검사
    token = split_header_token(request)

    # 토큰이 레디스에 존재 - 인증된 사용자
    if token in cache:
        value = cache.get(token)
        print(value)
        return True
    else:
        return False

# 로그아웃
class LogoutAPIView(APIView):
    def get(self, request):
        token = split_header_token(request)
        print(token)

        is_Auth = token_authentication(request)

        # 레디스에 저장했던 토큰 삭제
        if is_Auth:
            if token in cache:
                cache.delete(token)
                return Response({'result_message': 'Logout Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'result_message' : 'Logout Fail'}, status=status.HTTP_200_OK)



# 회원 정보 조회 & 수정
#@method_decorator(login_required)
class ProfileAPIView(APIView):
    def get(self, args, **kwargs):

        #token_authentication(request)

        try :
            user_id = self.kwargs['user_id']
            # 사용자 pk로 현재 user_id 가져옴
            user_info = UserModelSerializer(User.objects.get(id=user_id))
        except User.DoesNotExist:
            return Response({'result_message': 'Your information Does Not Exists'}, status=status.HTTP_200_OK)

        return Response({'result_message' : 'Your Information', 'Info' : user_info.data}, status=status.HTTP_200_OK)

    def post(self, args, **kwargs):
        try:
            user_id = self.kwargs['user_id']
            user_info = UserModelSerializer(User.objects.get(id=user_id))

        except User.DoesNotExist:
            return Response({'result_message': 'Your information Does Not Exists'}, status=status.HTTP_200_OK)

        # TODO TokenAuthentication 함수 호출f

        #token_authentication(request)

        #try :
          #  user_id = self.kwargs['user_id']


