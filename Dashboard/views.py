from django.shortcuts import render
from django.http import HttpRequest
import requests
from requests.exceptions import HTTPError
from django.contrib.auth import models
# import json
import datetime
from . import models as mod

# Create your views here.

def index(request):
    return render(request,'dashboard.html')

def courses(request):
    return render(request,'courses.html')

def assignments(request):
    return render(request,'assignments.html')

def announcements(request):
    return render(request,'announcements.html')

def grades(request):
    return render(request,'grades.html')