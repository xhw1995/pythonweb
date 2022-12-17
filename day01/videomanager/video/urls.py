# 子路由

from django.urls import path
from video.views import index
# 固定写法 urlpatterns = []
urlpatterns =[
    # path('路由', 视图函数名)
    path('index/', index),
]