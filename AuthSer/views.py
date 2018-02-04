from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from .serializers import UserModelSerializer
from .models import User
import json


# Create your views here.
# 회원가입 - csrf_exempt 때문에 FBV로 구현
@api_view(['GET','POST'])
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        received = json.dumps(request.data) #받은 json data 확인을 위함
        print(received)

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

        # 사용자가 입력한 비밀번호가 DB에 저장된 비밀번호와 같은지 비
        if request.data['password'] == user_id.data['password']:
            #TODO 토큰발행
            return Response({'Login_Success' : user_id.data},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'result_message' : 'Invalid Password. Please Check your password.'},status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    def get(self, request):
        #TODO 저장한 토큰 레디스에서 삭제
        return Response({'result_message' : 'Logout Success'}, status=status.HTTP_200_OK)

