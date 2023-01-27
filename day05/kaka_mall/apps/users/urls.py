from django.urls import path
from apps.users import views

urlpatterns = [
    # 判断用户是否重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    # 注册
    path('register/', views.RegisterView.as_view()),
]