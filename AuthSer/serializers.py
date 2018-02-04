#-*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User

class UserModelSerializer(ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    #created_time = serializers.DateTimeField()
    #modified_time = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ['id','user_email','password','user_name','user_tel','created_time','modified_time']