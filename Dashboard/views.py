from os import name
from django.shortcuts import render
from django.http import HttpRequest, request
import requests
from requests.exceptions import HTTPError
from django.contrib.auth import models
# import json
import datetime
import markdown
from . import models as mod
from . import forms 

# Create your views here.

def index(request):
    return render(request,'dashboard.html')

def courses(request):
    return render(request,'courses.html')

def assignments(request):
    assignment_dict = {}
    for asgn in mod.Assignments.objects.all():
        assignment_dict[asgn.name] = asgn.description
    return render(request,'assignments.html', {'data' : assignment_dict})

def assignment_submission(request):
    if request.method == 'POST':
        form = forms.AssignmentSubmissionForm(request.POST, request.FILES)
        print(form.is_valid())
        print(form.cleaned_data.get('name'))
        if form.is_valid():
            if(mod.Courses.objects.filter(course_name = "trial 1a")):
                course1 = mod.Courses.objects.get(course_name = "trial 1a")
            else:
                course1 = mod.Courses(course_name = "trial 1a")
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

            if mod.Enrollment.objects.filter(profile = profile1) and mod.Enrollment.objects.filter(course = course1):
                print("Enrollment Exists")
                enrollment = mod.Enrollment.objects.get(profile = profile1, course = course1)
            else:
                enrollment = mod.Enrollment(profile = profile1)
                enrollment.course = course1
                enrollment.save()
            if(mod.Assignments.objects.filter(enrollment=enrollment, name="Lab1")):
                asgn1 = mod.Assignments.objects.get(enrollment=enrollment, name="Lab1")
            else:
                asgn1 = mod.Assignments(enrollment=enrollment, name="Lab1")
                asgn1.save()
            for file in request.FILES.getlist('files'):
                file1 = mod.AssignmentFiles(assignment=asgn1, file=file)
                file1.save()
            print("all ok")

        return render(request, 'assignment_submission.html', {'form' : form})
    else:
        form = forms.AssignmentSubmissionForm()
    return render(request, 'assignment_submission.html', {'form' : form})

def assignment_creation(request):
    if request.method == 'POST':
        form = forms.AssignmentCreationForm(request.POST)
        if form.is_valid():
            if(mod.Courses.objects.filter(course_name = "trial 1a")):
                course1 = mod.Courses.objects.get(course_name = "trial 1a")
            else:
                course1 = mod.Courses(course_name = "trial 1a")
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

            if mod.Enrollment.objects.filter(profile = profile1) and mod.Enrollment.objects.filter(course = course1):
                print("Enrollment Exists")
                enrollment = mod.Enrollment.objects.get(profile = profile1, course = course1)
            else:
                enrollment = mod.Enrollment(profile = profile1)
                enrollment.course = course1
                enrollment.save()

            print(enrollment.profile)
            print(enrollment.course)
            print(enrollment.grade)
            assignment = mod.Assignments(enrollment=enrollment)
            assignment.name = form.cleaned_data.get('assignment_name')
            assignment.description = markdown.markdown(form.cleaned_data.get('description'))
            assignment.save()

            return render(request,'assignments.html')
    else:
        form = forms.AssignmentCreationForm()
    return render(request, 'assignment_creation.html',{'form':form})

def announcements(request):
    return render(request,'announcements.html')

def grades(request):
    return render(request,'grades.html')

def profile(request):
    courses_list={}
    #ADD course lists here
    return render(request,'profile.html', courses_list)

def settings(request):
    return render(request,'settings.html') 

def add_course(request, sample_input):
    if(mod.Courses.objects.filter(course_name = "trial 1a")):
        course1 = mod.Courses.objects.get(course_name = "trial 1a")
    else:
        course1 = mod.Courses(course_name = "trial 1a")
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

    if mod.Enrollment.objects.filter(profile = profile1) and mod.Enrollment.objects.filter(course = course1):
        print("Enrollment Exists")
        enrollment = mod.Enrollment.objects.get(profile = profile1, course = course1)
    else:
        enrollment = mod.Enrollment(profile = profile1)
        enrollment.course = course1
        enrollment.save()

    print(enrollment.profile)
    print(enrollment.course)
    print(enrollment.grade)






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

