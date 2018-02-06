from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from .serializers import UserModelSerializer
from .models import User
import json,jwt,datetime
from django.conf import settings
from django.core.cache import cache



# Create your views here.
# 회원가입 - csrf_exempt 때문에 FBV로 구현
@api_view(['GET','POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        received = json.dumps(request.data) #받은 json data 확인을 위함
        print(received)

        #Model에 저장 위해 직렬화
        serializer = UserModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'received':request.data},status=status.HTTP_201_CREATED)
        return Response({'result_message':'Email Already exists'},status=status.HTTP_400_BAD_REQUEST)

    else: #GET
        serializer = UserModelSerializer(User.objects.all(), many=True)
        return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
#로그인 - csrf_exempt때문에 FBV로 구현
def login(request):
    if request.method == 'POST':
        try:
            received = json.dumps(request.data)  # 받은 json data 확인을 위함
            print(received)

            # 사용자가 입력한 이메일 확인
            user_id = UserModelSerializer(User.objects.get(user_email=request.data['user_email']))
            #return Response({'result_message' : user_id.data},status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'result_message' : 'Your Email Does Not Exists'},status=status.HTTP_404_NOT_FOUND)

        #print(request.data['password'])

        #json_pwd = JSONRenderer().render(user_id.data)
        #print(json_pwd)
        #print(user_id.data['password'])

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

            token = {'token' : jwt.encode(payload, "SECRET_KEY", algorithm='HS256') }

            print(token)





            # TODO 레디스에 토큰 저장

            # Client 에게 토큰을 json에 담아 보냄
            return Response({'Login_Success' : token},status=status.HTTP_200_OK)
        else:
            return Response({'result_message' : 'Invalid Password. Please Check your password.'},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def token_authentication(request):
    # 헤더에 담긴 토큰 레디스에 있는지 검사
    #if request.method == 'POST' :
    pass

class LogoutAPIView(APIView):
    def get(self, request):
        #TODO 저장한 토큰 레디스에서 삭제
        return Response({'result_message' : 'Logout Success'}, status=status.HTTP_200_OK)



"""
# 토큰 생성
def create_jwt(UserModelserializer):
    payload = {
        'user_email': user_id.data['user_email'],
        'user_name': user_id.data['user_name'],
        'password': user_id.data['password'],
        'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    token = {'token': jwt.encode(payload, "SECRET_KEY", algorithm='HS256')}

    return token
    """

