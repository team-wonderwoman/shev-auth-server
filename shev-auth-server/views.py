from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from AuthSer.serializers import UserModelSerializer
from AuthSer.models import User
import json

# Create your views here.
# 회원가입
class SignUpAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get(self, request):
        serializer = UserModelSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserModelSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):
    def get(self, request, user_email):
        post = get_object_or_404(User, user_email=user_email)
        serializer = UserModelSerializer(post)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserModelSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)




