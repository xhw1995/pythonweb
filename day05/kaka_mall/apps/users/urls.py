from django.urls import path
from apps.users import views

urlpatterns = [
    # 判断用户是否重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    # 注册
    path('register/', views.RegisterView.as_view()),
    # 登录
    path('login/', views.LoginView.as_view()),
    # 退出
    path('logout/', views.LogoutView.as_view()),
    # 用户中心
    path('info/', views.CenterView.as_view()),
    # 邮箱
    path('emails/', views.EmailView.as_view())
]