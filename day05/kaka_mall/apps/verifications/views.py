from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

"""
前端
    拼接一个url，给一个img。img会发起请求
    url = http://ip:port/image_codes/uuid

后端
    请求：接收url中的uuid
    业务逻辑：生成 图片验证码 和 图片二进制，用redis保存图片验证码
    相应：返回 图片二进制
    路由：GET image_codes/uuid/

步骤
    1 接收url中的uuid
    2 生成 图片验证码 和 图片二进制
    3 redis保存图片验证码
    4 返回 图片二进制
"""

class ImageCodeView(View):

    def get(self, request, uuid):
        # 1 接收url中的uuid

        # 2 生成 图片验证码 和 图片二进制
        from libs.captcha.captcha import captcha
        """
        text：图片验证码
        image：图片二进制
        """
        text, image = captcha.generate_captcha()
        # 3 redis保存图片验证码
        # 3.1 链接redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('captcha')
        # 3.2 指令操作
        redis_cli.setex(uuid, 100, text)    # 100秒到期
        # 4 返回 图片二进制
        # 图片是二进制，不能返回JSON数据
        """
        content_type：别名MIME类型，响应体数据类型
        语法形式：大类/小类
        图片：image/jpeg，image/git，image/png
        """
        return HttpResponse(image,content_type='image/jpeg')