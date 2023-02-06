from django.http import HttpResponse, JsonResponse
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

"""
前端
    用户输入 手机号和图片验证码 后，前端发送axios请求

后端
    请求：接收请求，获取请求参数（路由：手机号；查询字符串：UUID、图片验证码）
    业务逻辑：验证参数，验证图片验证码，生成短信验证码，保存短信验证码，发送短信验证码
    响应：返回JSON数据
        {'code':0, 'errmsg':'ok'}
    路由： GET 

步骤：
    1 获取请求参数
    2 验证参数
    3 验证图片验证码
    4 生成短信验证码
    5 保存短信验证码
    6 发送短信验证码
    7 返回响应

debug 模式（调试模式）
debug + 断点：可以看到程序执行过程
在函数体的第一行添加断点！！！
"""
class SmsCodeView(View):
    def get(self, request, mobile):
        # 1 获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2 验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': "参数不全"})
        # 3 验证图片验证码
        # 3.1 链接Redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('captcha')
        # 3.2 获取Redis数据
        redis_image_code = redis_cli.get('uuid')
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': "图片验证码已过期"})
        # 3.3 对比数据
        """
        注意
            redis_image_code：bytes类型
            image_code：str类型
        两者类型不同，需要转换类型
        以防万一，两者都小写处理
        """
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': "图片验证码错误"})
        # 5.3 提取发送短信的标记
        send_flag = redis_cli.get('send_flag_%s'%mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': "不要频繁发送短信"})
        # 4 生成oo短信验证码
        from random import randint
        sms_code = '%06d'%randint(0, 999999)

        # # 5.1 保存短信验证码
        # redis_cli.setex(mobile, 300, sms_code)
        # # 5.2 添加一个发送标记：有效期60秒，内容随意
        # redis_cli.setex('send_flag_%s'%mobile, 60, 1)

        # 5.4 pipeline管道 实现5.1和5.2
        # 5.4.1 新建一个管道
        pipeline = redis_cli.pipeline()
        # 5.4.2 管道收集指令
        pipeline.setex(mobile, 300, sms_code)
        pipeline.setex('send_flag_%s'%mobile, 60, 1)
        # 5.4.3 管道执行指令
        pipeline.execute()

        # 6.1 发送短信验证码
        #from libs.yuntongxun.sms import CCP
        #CCP.send_template_sms(mobile, [sms_code, 5], 1)
        # 6.2 celery异步发送短信（替换6.1）
        from celery_tasks.sms.tasks import celery_send_sms_code
        """
        因为被task装饰器装饰，有delay函数
        delay的参数 等同于 任务（函数）的参数
        """
        celery_send_sms_code.delay(mobile, sms_code)

        # 7 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
