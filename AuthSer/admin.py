from django.contrib import admin
from .models import User
from chat.models import Group,GroupMember,Topic,TopicMember,TopicMessage
# Register your models here.

admin.site.register(User)


admin.site.register(Group)
admin.site.register(GroupMember)
# admin.site.register(ChatRoom)
# admin.site.register(ChatMember)
# admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(TopicMember)
admin.site.register(TopicMessage)