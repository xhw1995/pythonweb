from django.urls import path
from book import views

from django.urls import converters
from django.urls.converters import register_converter

# 1 定义 自定义转换器
class ShopConverter:
    # 验证数据的关键：正则
    regex = '1[3-9]\d{9}'

    # to_python将验证无误的数据，给视图函数
    def to_python(self, value):
        return int(value)

    # to_url将匹配结果用于反向解析传值时使用（了解）
    #def to_url(self, value):
    #    return str(value)
# 2 注册 转换器后，才能在path中使用
# converter：转换器类
# type_name：转换器名字
register_converter(ShopConverter, "shop_check")

urlpatterns = [
    path('create_book/', views.create_book),

    # <转换器名字:变量名>
    # 转换器会对变量数据进行 正则验证
    path('<int:city_id>/<shop_check:shop_id>/', views.shop),
    path('register/', views.register),
    path('json/', views.json),
    path('method/', views.method),
    path('response/', views.response),
    path('set_cookie/', views.set_cookie),
    path('get_cookie/', views.get_cookie),
    path('set_session/', views.set_session),
    path('get_session/', views.get_session),
    path('login/', views.login),

    # 类视图
    path('123login/', views.LoginView.as_view()),
    path('order/', views.OrderView.as_view()),
]