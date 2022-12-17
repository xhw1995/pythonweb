from django.shortcuts import render

# Create your views here.
"""
视图:定义在view.py中的一个函数
2个要求：
    1 视图函数的第一个参数是接受请求。请求（request）对应的是django.http中的HttpRequest的类对象
    2 必须返回一个响应。响应对应的是django.http中的HttpResponse的类对象
"""
from django.http import HttpRequest
from django.http import HttpResponse

# 希望用户通过 http://127.0.0.1:8000/index/ 来访问视图函数
def index(request):
    # return HttpResponse('Hello World!')

    """
    render(request, template_name, context=None, content_type=None, status=None, using=None)
    render：渲染模板
    参数详解
    request：请求
    template_name：模板名称
    context=None：
    """
    context = {
        'title': "点我一下，猜你想看"
    }
    return render(request, 'Video/index.html', context=context)
