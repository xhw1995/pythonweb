from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from book.models import BookInfo


def create_book(request):
    book = BookInfo.objects.create(
        name='雪中悍刀行',
        pub_date='2000-1-1',
        readcount=100,
    )
    return HttpResponse("create")