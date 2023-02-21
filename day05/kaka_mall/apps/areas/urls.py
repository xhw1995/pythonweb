from django.urls import path
from apps.areas import views

urlpatterns = [
    # 查询省份信息
    path('areas/', views.AreaView.as_view()),
    # 查询市、区县信息
    path('areas/<id>/', views.SubAreaView.as_view()),
]