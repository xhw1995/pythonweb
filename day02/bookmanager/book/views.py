from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    # 此处完成增删改查操作
    return HttpResponse("书籍是人类进步的阶梯！")