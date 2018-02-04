from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
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
        received = json.dumps(request.data)  # 받은 json data 확인을 위함
        print(received)

        serializer = UserModelSerializer(User.objects.get(user_email=received['user_email']))




"""
class SignUpAPIView(APIView):
    #authentication_classes = [DisableCSRF]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get(self, request):
        serializer = UserModelSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        dum_res = json.dumps(request.data)
        print(dum_res)
        #result = JSONParser.parse(request.data)
        #result = json.loads(request.data)

        #print(result['user_email'])

        #return Response({'received' : request.data})

        serializer = UserModelSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class LoginAPIView(APIView):
    def get(self, request):
        #post = get_object_or_404(User, user_email=user_email)
        #serializer = UserModelSerializer(post)
        return Response({'request' : request.data})

    def post(self, request):
        return Response({'received' : request.data})
    
        data = JSONParser().parse(request)
        try:
            userID = data['userID']
            qs = User.objects.get(user_email=userID)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

       #if qs.password == data['password']:
            # TODO 토큰 발행
"""




