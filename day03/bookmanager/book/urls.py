from django.urls import path
from book import views

urlpatterns = [
    path('create_book', views.create_book),
]