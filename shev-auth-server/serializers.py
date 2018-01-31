#-*- coding:utf-8 -*-
from rest_framework.serializers import ModelSerializer
from AuthSer.models import User

class UserModelSerializer(ModelSerializer):
    class Meta:
        models = User
        fields = ['id','user_email','password','user_name','user_tel','created_time','modified_time']

