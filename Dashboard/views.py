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
    course1 = mod.Courses(course_name = "trial 1")
    course2 = mod.Courses(course_name = "trial 2")
    course3 = mod.Courses(course_name = "trial 3")
    course4 = mod.Courses(course_name = "trial 4")
    course1.save()
    course2.save()
    course3.save()
    course4.save()


    profile1 = mod.Profile.objects.get(user = request.user)

    profile1.courses.add(course1)
    print("HERE")
    profile1.courses.add(course2)
    profile1.courses.add(course3)
    profile1.courses.add(course4)
    data = {
        "profileq":profile1.courses.all(),
        "course":course1.course_name
    }
    return render(request,'courses.html', data)

def assignments(request):
    return render(request,'assignments.html')

def announcements(request):
    return render(request,'announcements.html')

def grades(request):
    return render(request,'grades.html')