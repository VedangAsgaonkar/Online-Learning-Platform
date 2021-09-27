from . import views
from .views import *
from django.contrib import admin
from django.urls import path, include 

urlpatterns=[
    # path("",views.signup_view,name="home"),
    #path("login/",include('django.contrib.auth.urls')),
    path("signup/",views.signup_view,name="signup"),
]
