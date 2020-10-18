from django.urls import path
from . import views

urlpatterns = [

    path('display_news', views.display_news)


]