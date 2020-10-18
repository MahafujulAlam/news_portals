from django.shortcuts import render
from Content.models import Blog
from rest_framework import response
from django.http import HttpResponse
# from .forms import PostForm

# Create your views here.


def display_news(request):
    data = Blog.objects.all()[:50]
    # post = PostForm()
    print(data, "datadata data")

    url = "http://127.0.0.1:8000/media/"
    return render(request, 'blog_news/index.html',{"data":data, "url":url})