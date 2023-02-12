import json
import re

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
from users.models import User
from django.http import JsonResponse
import re

class UsernameCountView(View):

    def get(self, request, username):
        # 1 接收用户名，对用户名判断

        # 1.1 正则表达式 判断用户名
        #if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #    return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求！'})

        """
        1.2 自定义转换器，判断用户名，
            utils/converters.py：自定义转换器
            kaka_mall/urls.py：注册转换器
            apps/users/urls.py：使用转换器
        """

        # 2 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

"""
注册业务
前端
    用户输入 用户名、密码、确认密码、手机号、是否同意协议后，会点击注册按钮
    前端发送axios请求

后端（不相信前端提交的任何数据！！！）
    请求：接收请求(JSON)，获取数据
    业务逻辑：验证数据，数据入库
    相应：JSON{'code':0, 'errmsg':'ok'}
    路由  POST    register/
    
步骤
    1 接收请求（POST----JSON）
    2 获取数据
    3 验证数据
        3.1 用户名：满足正则，不能重复
        3.2 密码：满足规则
        3.3 确认密码：和密码一致
        3.4 手机号：满足规则，不能重复
        3.5 协议：需要同意
    4 数据入库
    5 返回相应
"""
import json
class RegisterView(View):
    def post(self, request):
        # 1 接收请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        # 2 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # 3 验证数据
        # all([xxx, xxx, xxx])：all里的元素只要是None、返回False；否则返回True
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': "参数不全"})
        # 3.1 用户名：满足正则，不能重复
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': "用户名格式错误"})
        # 3.2 密码：满足规则
        if not re.match('[a-zA-Z0-9]{8,20}', password):
            return JsonResponse({'code': 400, 'errmsg': "密码格式错误"})
        # 3.3 确认密码：和密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': "两次密码不一致"})
        # 3.4 手机号：满足规则，不能重复
        if not re.match('1[3-9]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': "手机号码格式错误"})
        # 3.5 协议：需要同意
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': "请同意相关协议"})

        # 数据入库
        """
        方法一
        user = User()
        user.save()
        
        方法二
        user = User.objects.create()
        
        以上方法都可以数据入库，但是不能密码加密，要加密需要使用以下方法
        user = User.objects.create_user()
        """
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': "注册失败"})

        """
        1 注册成功，立刻登录
            状态保持
                1.1 客户端存储信息 cookie
                1.2 服务存储信息使用 Session
        2 注册成功，单独登录
        """
        # Django 提供状态保持方法
        from django.contrib.auth import login
        # 状态保持 -- 登录用户的状态保持
        login(request, user)

        # 5 返回相应
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})

"""
登录
前端
    用户输入用户名和密码后，点击登录按钮。前端发送axios请求

后端
    请求：接收数据，验证数据
    业务逻辑：验证用户名和密码，session
    响应：返回JSON数据

步骤
    1 接收数据
    2 验证数据
    3 验证用户名和密码
    4 session
    5 判断是否记住登录
    6 返回响应
"""
class LoginView(View):
    def post(self, request):
        # 1 接收数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2 验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': "参数不全"})
        # 2.1 确定是根据 用户名 还是 手机号 查询
        """
        通过修改 User.USERNAME_FIELD 字段，影响 authenticate 的查询
        """
        import re
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3 验证用户名和密码
        """
        方法1
        通过模型，根据用户名来查询
        User.objects.get(username=username)
        
        方法2
        系统提供方法 authenticate
        authenticate 传递用户名和密码
        正确：返回User信息
        错误：返回None
        """
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': "用户名或密码错误"})
        # 4 session
        from django.contrib.auth import login
        login(username, password)
        # 5 判断是否记住登录
        # 实质就是设置 session的过期时间
        if remembered is True:
            # 记住登录 -- 2周 或 1个月
            request.session.set_expiry(None)
        else:
            # 不记住登录 -- 浏览器关闭 session过期
            request.session.set_expiry(0)
        # 6 返回响应
        response = JsonResponse({'code': 0, 'errmsg': "ok"})
        # 设置cookie信息：使首页显示用户信息
        response.set_cookie('username', username, max_age=3600*24)
        return response

"""
退出
前端
    用户点击退出按钮，前端发送一个axios delete请求

后端
    请求：无
    业务逻辑：退出
    响应：返回JSON数据
"""
class LogoutView(View):
    def delete(self, request):
        from django.contrib.auth import logout
        # 1 清除session信息
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': "ok"})
        # 2 清除cookie信息
        # 因为前端是根据cookie信息，判断用户是否登录，所以要清除
        response.delete_cookie('username')
        return response

"""
LoginRequiredMixin
    未登录用户 会返回 重定向
    重定向 并不是JSON数据
    
方法一 将LoginRequiredMixin类重写为LoginRequiredJSONMixin，让CenterView继承LoginRequiredJSONMixin
from django.contrib.auth.mixins import AccessMixin
class LoginRequiredJSONMixin(AccessMixin):
    # Verify that the current user is authenticated.
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 此处修改为返回JSON数据
            return JsonResponse({'code': 400, 'errmsg': "用户尚未登录"})
        return super().dispatch(request, *args, **kwargs)

方法二 定义LoginRequiredJSONMixin类，继承LoginRequiredMixin。重写 handle_no_permission方法
from django.contrib.auth.mixins import LoginRequiredMixin
class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': "用户尚未登录"})
        
通用功能放入 utils.views 中
"""
from utils.views import LoginRequiredJSONMixin
class CenterView(LoginRequiredJSONMixin, View):
    def get(self, request):

        info_data = {
            """
            request.user 就是已登录的用户信息
            来源于中间件 django.contrib.auth.middleware.AuthenticationMiddleware
            系统会判断 如果是登录用户，则获取 登录用户对应的 模型实例数据
            如果不是登录用户，则request.user = AnonymousUser() 匿名用户
            """
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return JsonResponse({'code': 0, 'errmsg': "ok", 'info_data': info_data})

"""
需求
    1 保存邮箱地址
    2 发送一封激活邮件
    3 用户激活邮件
    
前端
    用户输入邮箱后，点击保存。此时发送axios请求

后端
    请求：接收请求，获取数据
    业务逻辑：保存邮箱地址，发送激活邮件
    响应：返回JSON code=0
    路由：PUT请求

步骤
    1 接收请求
    2 获取数据
    3 保存邮箱地址
    4 发送激活邮件
    5 返回响应
"""
class EmailView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 1 接收请求
        # put 和 post类似，数据存于body
        data = json.loads(request.body.decode())

        # 2.1 获取数据
        email = data.get('email')
        # 2.2 验证邮箱
        if not email:
            return JsonResponse({'code': 400, 'errmsg': "缺少email参数"})
        if not re.match('^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$ ', email):
            return JsonResponse({'code': 400, 'errmsg': "email参数有误"})
        # 3 保存邮箱地址
        user = request.user  # user / request.user 就是 登录用户的实例对象
        user.email = email
        user.save()
        # 4 发送激活邮件
        from django.core.mail import send_mail
        """
        参数
            subject：邮件标题
            message：邮件正文
            from_email：发件人
            recipient_list：收件人列表
            html_message：多媒体邮件正文，可以是html字符串
        """
        subject = "美多商城激活邮件"
        message = "点击按钮，进行激活<a href='http://www.kaka.cn'>点击激活</a>"
        from_email = "美多商城<qi_rui_hua@163.com>"
        recipient_list = ['2249932727@qq.com']
        # 邮件内容是 html时，需要使用html_message
        html_message = "点击按钮，进行激活<a href='http://www.kaka.cn'>点击激活</a>"
        send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email, recipient_list=recipient_list)
        # 5 返回响应
        return JsonResponse({'code': 0, 'errmsg': "ok"})

"""
1 设置邮件服务器
    开启163邮箱服务器
    
2 设置邮件发送的配置信息
    # 让django的哪个类发送邮件
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # 发送邮件服务器
    EMAIL_HOST = 'smtp.163.com'
    # 发送邮件端口号
    EMAIL_PORT = 25
    # 发送邮件的邮箱
    EMAIL_HOST_USER = 'qi_rui_hua@163.com'
    # 邮箱中设置的客户端授权码
    EMAIL_HOST_PASSWORD = '123456abc'

3 调用send_mail方法
"""