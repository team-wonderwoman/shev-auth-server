from django.conf.urls import url
from . import views
from django.views.decorators import csrf
# AuthSer/urls.py

urlpatterns = [
    url(r'^signup/$',views.signup),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.LogoutAPIView.as_view()),
]