from django.conf.urls import url
from . import views

# AuthSer/urls.py

urlpatterns = [
    url(r'^signup/$', views.SignUpAPIView.as_view()),
    url(r'^login/$',views.LoginAPIView.as_view()),

]