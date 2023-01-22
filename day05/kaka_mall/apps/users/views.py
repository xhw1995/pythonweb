from django.shortcuts import render

# Create your views here.

"""
判断用户是否重复的功能
前端
    用户输入用户名后，失去焦点，发送一个ajax请求

后端思路
    请求：接收用户名
    业务逻辑：根据用户名，查询数据库，如果查询结果为0，说明没有注册；如果大于0，则已注册
    响应：返回JSON数据
        (code:0,count:0/1,errmsg:ok)
    路由：GET    usernames/<username>/count/
步骤
    1 接收用户名
    2 根据用户名查询数据库
    3 返回响应
"""
from django.views import View
from apps.users.models import User
from django.http import JsonResponse

class UsernameCountView(View):

    def get(self, request, username):
        # 1 接收用户名
        # 2 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
