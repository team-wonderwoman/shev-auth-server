from django.contrib import admin
from AuthSer.models import User

# Register your models here.
# 관리자 페이지에 User 테이블 등록
admin.site.register(User)