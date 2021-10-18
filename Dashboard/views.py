from os import name
import os
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpRequest, request
import requests
from requests.exceptions import HTTPError
from django.contrib.auth import models
from django.contrib.auth.models import User
# import json
import datetime
import markdown
from . import models as mod
from . import forms 
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def index(request):
    # subject = 'welcome to GFG world'
    # message = f'Hi {request.user.username}, thank you for registering in geeksforgeeks.'
    # EMAIL_HOST_USER = 'technologic.itsp@gmail.com'
    # email_from = EMAIL_HOST_USER
    # recipient_list = ['vedanga2015@gmail.com', ]
    # send_mail( subject, message, email_from, recipient_list )

    courses_dict = {}
    if mod.Profile.objects.filter(user = request.user):
        profile = mod.Profile.objects.get(user = request.user)
    else:
        profile = mod.Profile(user = request.user)
        profile.save()
    for course in profile.courses.all():
        courses_dict[course.course_name] = "course.info"
    # print(courses_dict)
    return render(request,'dashboard.html', {'data' : courses_dict})

def courses(request, input_course_name = "DEFAULT"):
    if(mod.Courses.objects.filter(course_name = input_course_name)):
        course = mod.Courses.objects.get(course_name = input_course_name)
    data={}
    data['name'] = input_course_name
    data['info'] = course.course_info
    return render(request,'courses.html', data)

def assignments(request, course_name):
    assignment_dict = {}
    course = mod.Courses.objects.get(course_name = course_name)
    if(mod.Assignments.objects.filter(course=course)):
        for asgn in mod.Assignments.objects.all() :
            if(asgn.course == course):
                assignment_dict[asgn.name] = asgn.description
    return render(request,'assignments.html', {'data' : assignment_dict, 'course' : course_name})

def assignment_submission(request, course_name ,name):
    if request.method == 'POST':
        print("TEST")
        form = forms.AssignmentSubmissionForm(request.POST, request.FILES)
        print(form.is_valid())
        print(form.cleaned_data.get('name'))
        if form.is_valid():

            assignment = mod.Assignments.objects.get(course = course_name, name=name)
            for file in request.FILES.getlist('files'):
                file_name = course_name+'/'+name+'/'+str(request.user)
                file1 = mod.AssignmentFiles(assignment=assignment, file_name = file_name ,file=file)
                file1.save()
            print("all ok")

        return redirect('assignments', course_name=course_name ,permanent=True)
    else:
        enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
        if enrollment.isTeacher==True:
            return render(request, 'assignment_download.html')
        else:
            asgn_desc = mod.Assignments.objects.get(name=name).description
            form = forms.AssignmentSubmissionForm()
            return render(request, 'assignment_submission.html', {'form' : form, 'asgn' : asgn_desc})


def download_file(request):
    # fill these variables with real values
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def assignment_creation(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    if enrollment.isTeacher == False:
        return redirect('assignments', course_name = course_name,permanent=True)
    print("In here")
    if request.method == 'POST':
        form = forms.AssignmentCreationForm(request.POST)
        if form.is_valid():
            course1 = mod.Courses.objects.get(course_name = course_name)
            assignment = mod.Assignments(course=course1)
            assignment.name = form.cleaned_data.get('assignment_name')
            assignment.description = markdown.markdown(form.cleaned_data.get('description'))
            print(markdown.markdown(form.cleaned_data.get('description')))
            assignment.save()
            print("fine")

            return redirect('assignments', course_name = course_name,permanent=True)
    else:
        form = forms.AssignmentCreationForm()
    return render(request, 'assignment_creation.html',{'form':form})
    
def course_creation(request):
    if request.method == 'POST':
        print("HELLO")
        form = forms.CourseCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('course_name'))
            try:
                course_added = mod.Courses(course_name = form.cleaned_data.get('course_name'))
                course_added.access_code = form.cleaned_data.get('access_code')
                course_added.master_code = form.cleaned_data.get('master_code')
                course_added.course_info = form.cleaned_data.get('course_info')

                course_added.save()
            except Exception as e:
                print("Course already exists, collision!")

            if mod.Profile.objects.filter(user = request.user):
                print("Already Made")
                profile1 = mod.Profile.objects.get(user = request.user)
            else:
                profile1 = mod.Profile(user = request.user)
                print("CREATED")
                profile1.save()
                profile1 = mod.Profileobjects.get(user = request.user)

            profile1.courses.add(course_added)
            profile1.save()
            print("HERE")
            print(request.user)
            print(profile1.courses.all()[0])

            if mod.Enrollment.objects.filter(profile = profile1) and mod.Enrollment.objects.filter(course = course_added):
                print("Enrollment Exists")
                enrollment = mod.Enrollment.objects.get(profile = profile1, course = course_added)
            else:
                enrollment = mod.Enrollment(profile = profile1)
                enrollment.course = course_added
                enrollment.save()

            print(enrollment.profile)
            print(enrollment.course)
            print(enrollment.grade)

        return redirect('dashboard', permanent=True)
    else:
        form = forms.CourseCreationForm()
        return render(request, 'course_creation.html', {'form':form})
        
def course_access(request):
    if request.method == 'POST':
        form = forms.CourseEnrollForm(request.POST)
        if form.is_valid():
            profile = mod.Profile.objects.get(user = request.user)
            if mod.Courses.objects.filter(access_code = form.cleaned_data.get('access_code')):
                course = mod.Courses.objects.filter(access_code = form.cleaned_data.get('access_code')).first()
                if mod.Enrollment.objects.filter(profile = profile , course= course):
                    print("Already exists, checking for teacher role")
                    enroll = mod.Enrollment.objects.get(profile = profile , course = course)
                    if(course.master_code == form.cleaned_data.get('master_code')):
                        enroll.isTeacher = True
                        enroll.save()
                else:
                    enroll = mod.Enrollment(profile = profile , course = course)
                    if(course.master_code == form.cleaned_data.get('master_code')):
                        enroll.isTeacher = True
                        enroll.save()
                print('Added to course successfully')
            else:
                print('No course exists with access code: ', form.cleaned_data.get('access_code'))
        return redirect('dashboard', permanent = True)
    else:
        form = forms.CourseEnrollForm()
        return render(request , 'course_access.html',{'form': form})

def course_email(request, course_name):
    if request.method == 'POST':
        form = forms.CourseEmailForm(request.POST)
        if form.is_valid():
            course = mod.Courses.objects.get(course_name=course_name)
            email_list = [s.strip() for s in form.cleaned_data.get('emaillist').split(",")]
            subject = 'Course access code for course '+course_name
            message = 'Hi. This is an email giving you access to course '+course_name+'. Your access code is : ' + course.access_code
            EMAIL_HOST_USER = 'technologic.itsp@gmail.com'
            email_from = EMAIL_HOST_USER
            recipient_list = email_list
            send_mail( subject, message, email_from, recipient_list )           
        return redirect('dashboard', permanent = True)
    else:
        form = forms.CourseEmailForm()
        return render(request , 'course_email.html',{'form': form})   

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

