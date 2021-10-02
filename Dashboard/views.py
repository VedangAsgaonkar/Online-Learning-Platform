from django.shortcuts import render
from django.http import HttpRequest, request
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


def add_course(request, sample_input):
    if(mod.Courses.objects.filter(course_name = "trial 1")):
        course1 = mod.Courses.objects.get(course_name = "trial 1")
    else:
        course1 = mod.Courses(course_name = "trial 1")
        course1.save()
    if mod.Profile.objects.filter(user = "prats"):
        print("Already Made")
        profile1 = mod.Profile.objects.get(user = "prats")
    else:
        profile1 = mod.Profile(user = "prats")
        profile1.save()

    profile1.courses.add(course1)
    profile1.save()
    print("HERE")
    print(request.user)
    print(profile1.courses.all()[0])
    print(sample_input)
    data = {
        "profileq":profile1.courses.all(),
        "course":course1.profile_set.all(),
    }
    return render(request, 'courses.html', data)

def create_profile():
    new_profile = mod.Profile(user = request.user)
    new_profile.save()
    ##To be called only after signup and nowhere else

def create_course(name):
    new_course = mod.Courses(course_name = name)
    new_course.save()
    ###Store master variable inside the course_user pair

def add_course_to_profile(course_name):
    #called means verified to add, profile made and course exists
    profile = mod.Profile.objects.get(user = request.user)
    profile.courses.add(course_name)

def verify_access_code(input_course_name, access_code):
    # course exists is a prerequisite
    course = mod.Courses.objects.get(course_name = input_course_name)
    if course.code==access_code:
        return True
    else:
        return False

def grant_master_role(input_course_name, access_code):
    # course exists is a prerequisite
    course = mod.Courses.objects.get(course_name = input_course_name)
    if course.master_code==access_code:
        return True
    else:
        return False
#Need to store master_code variable inside the course

