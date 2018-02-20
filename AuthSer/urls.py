# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.views.decorators import csrf

from django.contrib.auth import views as auth_views

# AuthSer/urls.py

urlpatterns = [
    # api/signup
    # 사용자의 회원가입을 담당한다
    url(r'^signup/$',views.signup,name='signup'),

    # api/login
    # 사용자의 로그인을 담당한다
    url(r'^login/$', views.login,name='login'),

    # api/logout
    # 사용자의 로그아웃을 담당한다
    url(r'^logout/$', views.LogoutAPIView.as_view(),name='logout'),

    # api/profile/:user_id
    # 사용자의 회원 정보 조회, 수정을 담당한다
    url(r'^profile/(?P<user_id>\d+)/$', views.ProfileAPIView.as_view(),name='profile'),


    # api/:user_id/signout
    # 사용자의 회원 탈퇴를 담당한다
    url(r'^(?P<user_id>\d+)/signout/$', views.SignoutAPIView.as_view()),


    # # oauth
    # url(r'^google/$', views.oauth_login, name='oauth_login')
]