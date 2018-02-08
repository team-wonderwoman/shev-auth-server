# -*- coding: utf-8 -*-
from rest_framework import permissions

class IsAuthenticate(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated

    # superuser에게는 삭제권한만, 작성자에게는 수정권한만
    def has_object_permission(self, request, view, obj):
        # 조회(GET,HEAD,OPTIONS)에 대해서는 인증여부에 상관없이 허용
        if request.method in permissions.SAFE_METHODS:
            return True

