from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from book.models import BookInfo


def create_book(request):
    book = BookInfo.objects.create(
        name='剑来',
        pub_date='2001-1-1',
        readcount=50,
    )
    return HttpResponse("create")

def shop(request,city_id,shop_id):
    # 验证path中路径参数
    # 方法一：正则表达式
    #import re
    #if not re.match('\d{5}', shop_id):
    #    return HttpResponse("没有该店铺！")

    # 方法二：在urls中的path中利用 转换器 进行 正则验证

    print(city_id, shop_id)

    query_params = request.GET
    print(query_params)

    return HttpResponse("路西旗舰店")

def register(request):
    data = request.POST
    print(data)
    return HttpResponse("ok")

def json(request):
    body = request.body
    #print(body)
    # b'{\n    "name": "lucifer",\n    "age": 20\n}'

    body_str = body.decode()
    #print(body_str)
    """
    {
        "name": "lucifer",
        "age": 20
    }
    <class 'str'>
    """

    # JSON形式的字符串 可以转换为 Python字典
    import json
    body_dict = json.loads(body_str)
    print(body_dict)
    # {'name': 'lucifer', 'age': 20}

    # 请求头
    #print(request.META)
    print(request.META['SERVER_PORT'])
    #8000

    return HttpResponse("JSON")

def method(request):
    print(request.method)
    return HttpResponse('method')

def response(request):
    """
    HTTP status code must be an integer from 100 to 599
    1xx
    2xx
        200 成功
    3xx
    4xx 请求有问题
        403 禁止访问 权限问题
        404 找不到页面 路由问题
    5xx
    """
    #response = HttpResponse("response", status=200)
    #response["name"] = "lucifer"
    #return response

    info = {
        'name': 'lucifer',
        'age': '18',
        'gender': 'M',
    }
    friends = [
        {
            'name': 'Jack',
            'age': '15',
        },
        {
            'name': 'Mary',
            'age': '20',
        }
    ]
    """
    JsonResponse 将字典转换为JSON字符串
    data 返回响应数据 一般为字典类型
    """
    #response = JsonResponse(data=info)

    """
    错误：In order to allow non-dict objects to be serialized set the safe parameter to False
    传递非字典对象，需要将safe设置为False
    
    safe = True 表示data是字典数据
    JsonResponse可以将字典转换为JSON类型
    
    friends 是一个 字典列表 数据
    safe = False 表示出问题，自己负责
    """
    response = JsonResponse(data=friends, safe=False)

    # 验证JsonResponse的json.dumps
    # import json
    # data = json.dumps(friends)
    # response = HttpResponse(data)

    #return response

    # 重定向
    return redirect("https://www.baidu.com")


"""
Cookie
第一次请求携带 查询字符串
http://127.0.0.1:8000/set_cookie/?username=lucifer&password=123
服务器收到请求后，获取username，服务器设置cookie信息（信息包括username）
浏览器接收到服务器的响应后，将cookie保存

第二次之后，对 http://127.0.0.1:8000 的请求都会携带cookie信息，服务器可以读取cookie信息，来判断用户身份
"""
def set_cookie(request):
    # 1 获取查询字符串数据
    username = request.GET.get("username")
    password = request.GET.get("password")
    # 2 服务器设置cookie信息
    # 通过响应对象.set_cookie 方法
    response = HttpResponse("set_cookie")
    """
    set_cookie()参数
    key、value：
    max_age：单位秒数
    """
    response.set_cookie('name', username)
    response.set_cookie('password', password, max_age=3600)

    # 删除cookie：本质是将 max_age 设置为0
    response.delete_cookie('password')

    return response

def get_cookie(request):
    # 获取cookie
    print(request.COOKIES)
    # request.COOKIES 字典数据
    name = request.COOKIES.get('name')
    password = request.COOKIES.get('password')
    return HttpResponse(name, password)

"""
Session
第一次请求 http://127.0.0.1:8000/set_session/?username=lucifer 在服务器端设置session信息
服务器会生成一个sessionid的cookie信息
浏览器接收信息后，会保存cookie信息

第二次及之后的请求都会携带这个sessionid，服务器验证sessionid后，会读取相关数据，实现业务逻辑
"""
def set_session(request):
    # 1 获取username
    username = request.GET.get("username")
    # 2 请求设置session
    user_id = 1
    request.session['user_id'] = user_id
    request.session['username'] = username

    # clear 删除session里数据，但key会保留
    #request.session.clear()
    # flush 删除所有数据，包括key
    #request.session.flush()

    request.session.set_expiry(3600)

    return HttpResponse("set_session")

def get_session(request):

    #user_id = request.session['user_id']
    #username = request.session['username']

    # 用get()获取数据，可以减少异常发生
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    content = '{},{}'.format(user_id, username)

    return HttpResponse(content)

# 类视图
def login(request):
    if request.method == 'GET':
        return HttpResponse("GET")
    else:
        return HttpResponse("POST")

"""
类视图定义
class 类视图名字(View):
    def get(self, request):
        return HttpResponse('xxx')
    
    def http_method_lower(self, request):
        return HttpResponse('xxx')

1 继承自View
2 类视图中的方法 是采用 http方法小写来区分不同的请求
"""
from django.views import View
class LoginView(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')


"""
类视图的多继承重写dispatch

需求：
个人中心页面
如果用户已登录 可以访问
如果用户未登录 不应该访问，应跳转到登录页面
"""
from django.contrib.auth.mixins import LoginRequiredMixin

# LoginRequiredMixin：判断 只有登录用户才能访问页面
class OrderView(LoginRequiredMixin, View):
    def get(self, request):

        #isLogin = False
        #if not isLogin:
        #    return HttpResponse('尚未登录，跳转到登录页面')

        return HttpResponse('GET 我的订单页面，此页面必须登录')

    def post(self, request):
        return HttpResponse('POST 我的订单页面，此页面必须登录')

"""
多继承：Python、C++

"""