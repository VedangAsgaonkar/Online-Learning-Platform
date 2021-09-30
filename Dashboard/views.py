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
    if(mod.Courses.objects.filter(course_name = "trial 1")):
        course1 = mod.Courses.objects.get(course_name = "trial 1")
    else:
        course1 = mod.Courses(course_name = "trial 1")
        course1.save()
    if mod.Profile.objects.filter(user = "prats"):
        profile1 = mod.Profile.objects.get(user = "prats")
    else:
        profile1 = mod.Profile(user = "prats")
        profile1.save()

    profile1.courses.add(course1)
    profile1.save()
    print("HERE")
    data = {
        "profileq":profile1.courses.all(),
        "course":course1.profile_set.all(),
    }
    return render(request,'courses.html', data)

def assignments(request):
    return render(request,'assignments.html')

def announcements(request):
    return render(request,'announcements.html')

def grades(request):
    return render(request,'grades.html')