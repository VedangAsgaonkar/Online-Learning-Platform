from os import name
import shutil
import os
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpRequest, request
from pandas.core.indexing import convert_to_index_sliceable
import requests
from requests.exceptions import HTTPError
from django.contrib.auth import models, update_session_auth_hash
from django.contrib.auth.models import User
import datetime
import pytz
import threading
import markdown
from . import models as mod
from . import forms 
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from django.utils import timezone


EMAIL_HOST_USER = 'technologic.itsp@gmail.com'
email_from = EMAIL_HOST_USER

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

# Create your views here.

def index(request):
    courses_dict = {}
    asgn_remaining_dict = []
    asgn_remaining_dict1 = {}
    try:
        if mod.Profile.objects.filter(user = request.user):
            profile = mod.Profile.objects.get(user = request.user)
        else:
            profile = mod.Profile(user = request.user, email_id=request.user.member.email_id)
            profile.save()
        for course in profile.courses.all():
        
            enrollment = mod.Enrollment.objects.get(profile = profile, course = course)
            total_completed = 0
            total_course = 0
            for assignment in mod.Assignments.objects.filter(course = course) :
                total_course+= 1
                try:
                    x = mod.AssignmentCompleted.objects.get(enrollment = enrollment, assignment = assignment)
                    if not x.isCompleted and assignment.deadline != None:
                        if enrollment.isTeacher:
                            asgn_remaining_dict1[course.course_name] = [assignment.name ,assignment.deadline, True ]
                        elif enrollment.isAssistant and course.assistant_grading_privilege:
                            asgn_remaining_dict1[course.course_name] = [assignment.name ,assignment.deadline, True ]
                        elif not enrollment.isAssistant:
                            asgn_remaining_dict1[course.course_name] = [assignment.name ,assignment.deadline, False ]
                    else :
                        total_completed+=1
                except Exception as e:
                    print(e)
            if total_course==0:
                courses_dict[course.course_name] = [course.course_info , 100]
            else:
                courses_dict[course.course_name] = [course.course_info , total_completed/total_course*100]
        return render(request,'dashboard.html', {'data' : courses_dict , 'to_do': asgn_remaining_dict , 'to_do_dead': asgn_remaining_dict1})
    except:
        return redirect('signup')

def courses(request, input_course_name = "DEFAULT"):
    if(mod.Courses.objects.filter(course_name = input_course_name)):
        course = mod.Courses.objects.get(course_name = input_course_name)
    data={}
    data['name'] = input_course_name
    data['info'] = course.course_info
    return render(request,'courses.html', data)

def assignments(request, course_name):
    assignment_dict = {}
    content_dict = {}
    course = mod.Courses.objects.get(course_name = course_name)
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    if enrollment.isTeacher or (enrollment.isAssistant and course.assistant_grading_privilege):
        teacher = True
    else:
        teacher = False
    if(mod.Assignments.objects.filter(course=course)):
        for asgn in mod.Assignments.objects.all() :
            if(asgn.course == course):
                assignment_dict[asgn.name] = asgn.description
    if(mod.CourseContent.objects.filter(course=course)):
        for content in mod.CourseContent.objects.all() :
            if(content.course == course):
                content_dict[content.name] = content.description
    return render(request,'assignments.html', {'asgn_data' : assignment_dict,'content_data' : content_dict, 'course' : course_name, 'teacher':teacher})

def assignment_submission(request, course_name ,name):
    if request.method == 'POST':
        print("TEST")
        form = forms.AssignmentSubmissionForm(request.POST, request.FILES)
        print(form.is_valid())
        print(form.cleaned_data.get('name'))
        if form.is_valid():
            assignment = mod.Assignments.objects.get(course = course_name, name=name)
            # enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
            for file in request.FILES.getlist('files'):
                file_name = course_name+'/'+name+'/'+str(request.user)
                file1 = mod.AssignmentFiles(assignment=assignment, file_name = file_name ,file=file, profile = mod.Profile.objects.get(user = request.user))
                file1.save()
            print("all ok")
            id_list = [request.user.member.email_id]
            subject = "Assignment submission for " + name + " in course " + course_name
            message = "Successfully submitted assignment " + name + " in course " + course_name
            t3 = threading.Thread(target=send_email, args=(subject, message, email_from, id_list, None ))  
            t3.start()
            enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = mod.Courses.objects.get(course_name = course_name))
            assigncomplete = mod.AssignmentCompleted.objects.get(enrollment = enrollment , assignment =  assignment)
            assigncomplete.isCompleted = True
            assigncomplete.save()
        return redirect('assignments', course_name=course_name ,permanent=True)
    else:
        enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
        course = mod.Courses.objects.get(course_name = course_name)
        if enrollment.isTeacher==True or (enrollment.isAssistant and course.assistant_grading_privilege):
            return render(request, 'assignment_download.html')
        else:
            asgn_desc = mod.Assignments.objects.get(course = course_name,name=name).description
            form = forms.AssignmentSubmissionForm()
            assignment = mod.Assignments.objects.get(course = course_name, name=name)
            assigncomplete = mod.AssignmentCompleted.objects.get(enrollment = enrollment , assignment =  assignment)
            if mod.AssignmentFiles.objects.filter(assignment = mod.Assignments.objects.get(course = course_name , name = name), profile = mod.Profile.objects.get(user = request.user)):
                asgn_file = mod.AssignmentFiles.objects.filter(assignment = mod.Assignments.objects.get(course = course_name , name = name), profile = mod.Profile.objects.get(user = request.user)).first()
                return render(request, 'assignment_submission.html', {'form' : form, 'asgn' : asgn_desc, 'asgn_feedback': asgn_file.feedback,'asgn_grade': asgn_file.grade,'isCompleted' : assigncomplete.isCompleted})
                # change form above to editable assignment submission
            return render(request, 'assignment_submission.html', {'form' : form, 'asgn_name' : assignment.name, 'asgn' : asgn_desc, 'asgn_feedback': "Submit File for feedback ",'asgn_grade': "Not graded yet", 'asgn_deadline' : assignment.deadline} )

def create_barchart(x_data):
    imgdata = StringIO()
    imgdata.truncate(0)
    imgdata.seek(0)
    plt.hist(x_data)
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    plt.clf()
    return data 

def content_view(request,course_name,name):
    content = mod.CourseContent.objects.get(course = course_name,name=name)
    return render(request, 'content_view.html', {'content_name':content.name, 'content_desc':content.description})


def assignment_download(request,course_name,name):
    fl_path = 'files/'+course_name+'/'+name
    if request.method=='POST' and os.path.isdir(fl_path):
        output_filename = 'zipped/zip'
        shutil.make_archive(output_filename, 'zip', fl_path)

        zip_file = open(output_filename+'.zip', 'rb')
        return FileResponse(zip_file, filename=course_name+'_'+name+'_submissions.zip')
    else:
        fl_path = 'files/'+course_name+'/'+name
        cmd = "ls './" + fl_path + "'"
        try:
            subs = get_immediate_subdirectories(fl_path)
        except:
            subs = []
        assignment = mod.Assignments.objects.get(course = course_name,name=name)
        asgn_desc = assignment.description
        profile_set = set()
        grades = []
        for sub in mod.AssignmentFiles.objects.filter(assignment = assignment):
            if sub.profile not in profile_set:
                profile_set.add(sub.profile)
                if sub.grade != 'Not graded yet':
                    grades.append(float(sub.grade))
        print(grades)
        if len(grades) > 0 :
            is_graded = True
            grades = np.array(grades)
            mean = np.mean(grades)
            std = np.std(grades)
            plot = create_barchart(grades)
        else:
            is_graded = False
            mean = "Not graded"
            std = "Not graded"
            plot = "Not graded"
        return render(request, 'assignment_download.html', {'asgn' : asgn_desc, 'subs':subs , 'course_name': course_name , 'name':name, 'mean' : mean, 'std':std, 'plot' : plot, 'isgraded' : is_graded })


def assignment_feedback(request,course_name,name):
    if request.method=='POST':
        form = forms.AssignmentFeedbackForm(request.POST, request.FILES)
        if(form.is_valid()):
            assignment = mod.Assignments.objects.get(course = course_name , name = name)
            assignment_files = mod.AssignmentFiles.objects.filter(assignment = assignment)
            file = request.FILES.getlist('feedback_file')[0]
            ds = pd.read_csv(file)
            id_set = set()
            for i in ds.index:
                for assignment_profile in assignment_files.filter(profile = mod.Profile.objects.get(user = ds['name'][i])):
                    assignment_profile.feedback = ds['feedback'][i]
                    assignment_profile.grade = ds['grade'][i]
                    assignment_profile.marks = ds['marks'][i]
                    assignment_profile.save()
                id_set.add( mod.Profile.objects.get(user = ds['name'][i]).email_id )
            allCorrected = True
            for enrollment in mod.Enrollment.objects.filter(course = mod.Courses.objects.get(course_name = course_name), isTeacher = False) :
                allCorrected = allCorrected and mod.AssignmentCompleted.objects.get(enrollment = enrollment, assignment = assignment).isCompleted
                if not allCorrected :
                   break
            if allCorrected :
                for enrollment in mod.Enrollment.objects.filter(course = mod.Courses.objects.get(course_name = course_name), isTeacher = True) : 
                    x = mod.AssignmentCompleted.objects.get(enrollment = enrollment, assignment = assignment)
                    x.isCompleted = True
                    x.save()
            id_list = list(id_set)
            subject = "Feedback for assignment " + name + " in course " + course_name
            message = "View Feedback on BlueFire moodle"
            t4 = threading.Thread(target=send_email, args=(subject, message, email_from, id_list, None ))  
            t4.start()
            return redirect('assignments', course_name = course_name, permanent = True)
    else :
        form = forms.AssignmentFeedbackForm()
        return render(request,'feedback.html' , {'form': form})


def assignment_creation(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    course = mod.Courses.objects.get(course_name = course_name)
    if not (enrollment.isTeacher or (enrollment.isAssistant and course.assistant_creation_privilege)) :
        return redirect('assignments', course_name = course_name,permanent=True)
    print("In here")
    if request.method == 'POST':
        form = forms.AssignmentCreationForm(request.POST)

        if form.is_valid():
            course1 = mod.Courses.objects.get(course_name = course_name)
            assignment = mod.Assignments(course=course1)
            assignment.name = form.cleaned_data.get('assignment_name')
            assignment.weightage = form.cleaned_data.get('weightage')
            assignment.deadline = form.cleaned_data.get('deadline')
            print("fine")
            assignment.description = markdown.markdown(form.cleaned_data.get('description'))
            print(markdown.markdown(form.cleaned_data.get('description')))
            assignment.save()

            id_set = set()
            for e in mod.Enrollment.objects.filter(course = course1):
                profile_e = e.profile
                mail_e = profile_e.email_id
                if mail_e:
                    id_set.add(mail_e)
            id_list = list(id_set)
            print(id_list)
            subject = "New assignment created : " + form.cleaned_data.get('assignment_name') + " in course : " + course_name
            message = "Instructor " + str(request.user) + " has added a new assignment " + form.cleaned_data.get('assignment_name') + " in course " + course_name + ". Description :\n"
            html_message = "Instructor " + str(request.user) + " has added a new assignment " + form.cleaned_data.get('assignment_name') + " in course " + course_name + ". Description :<br>"+markdown.markdown(form.cleaned_data.get('description'))
            t2 = threading.Thread(target=send_email, args=(subject, message, email_from, id_list, html_message ))  
            t2.start() 
            e_iter = mod.Enrollment.objects.filter(course = course_name)
            for e in e_iter :
                x = mod.AssignmentCompleted(enrollment = e, assignment = assignment)
                x.save()
                print(x.isCompleted)
            return redirect('assignments', course_name = course_name,permanent=True)
    else:
        form = forms.AssignmentCreationForm()
    return render(request, 'assignment_creation.html',{'form':form})
	
def content_creation(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    course = mod.Courses.objects.get(course_name = course_name)
    if not (enrollment.isTeacher or (enrollment.isAssistant and course.assistant_creation_privilege)) :
        return redirect('assignments', course_name = course_name,permanent=True)
    print("In here")
    if request.method == 'POST':
        form = forms.ContentCreationForm(request.POST)

        if form.is_valid():
            course1 = mod.Courses.objects.get(course_name = course_name)
            content = mod.CourseContent(course=course1)
            content.name = form.cleaned_data.get('content_name')
            print("fine")
            content.description = markdown.markdown(form.cleaned_data.get('description'))
            print(markdown.markdown(form.cleaned_data.get('description')))
            content.save()

            id_set = set()
            for e in mod.Enrollment.objects.filter(course = course1):
                profile_e = e.profile
                mail_e = profile_e.email_id
                if mail_e:
                    id_set.add(mail_e)
            id_list = list(id_set)
            print(id_list)
            subject = "New course content added : " + form.cleaned_data.get('content_name') + " in course : " + course_name
            message = "Instructor " + str(request.user) + " has added new content " + form.cleaned_data.get('content_name') + " in course " + course_name + ". Description :\n"
            html_message = "Instructor " + str(request.user) + " has added new content " + form.cleaned_data.get('content_name') + " in course " + course_name + ". Description :<br>"+markdown.markdown(form.cleaned_data.get('description'))
            t6 = threading.Thread(target=send_email, args=(subject, message, email_from, id_list, html_message ))  
            t6.start() 
            return redirect('assignments', course_name = course_name,permanent=True)
    else:
        form = forms.ContentCreationForm()
    return render(request, 'content_creation.html',{'form':form})



def course_creation(request):
    if request.method == 'POST':
        print("HELLO")
        form = forms.CourseCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('course_name'), form.cleaned_data.get('assistant_can_grade_assignments'))
            try:
                course_added = mod.Courses(course_name = form.cleaned_data.get('course_name'))
                course_added.access_code = form.cleaned_data.get('access_code')
                course_added.master_code = form.cleaned_data.get('master_code')
                course_added.assistant_code = form.cleaned_data.get('assistant_code')
                course_added.course_info = form.cleaned_data.get('course_info')
                course_added.assistant_adding_privilege = form.cleaned_data.get('assistant_can_add_students')
                course_added.assistant_creation_privilege = form.cleaned_data.get('assistant_can_create_assignment')
                course_added.assistant_grading_privilege  = form.cleaned_data.get('assistant_can_grade_assignments')

                course_added.save()
            except Exception as e:
                print("Course already exists, collision!")

            if mod.Profile.objects.filter(user = request.user):
                print("Already Made")
                profile1 = mod.Profile.objects.get(user = request.user)
            else:
                profile1 = mod.Profile(user = request.user, email_id=request.user.member.email_id)
                print("CREATED")
                profile1.save()
                profile1 = mod.Profile.objects.get(user = request.user)

            profile1.courses.add(course_added)
            profile1.save()
            print("HERE")
            print(request.user)
            print(profile1.courses.all()[0])

            if mod.Enrollment.objects.filter(profile = profile1) and mod.Enrollment.objects.filter(course = course_added):
                print("Enrollment Exists")
                enrollment = mod.Enrollment.objects.get(profile = profile1, course = course_added)
                enrollment.isTeacher = True
                enrollment.save()
            else:
                enrollment = mod.Enrollment(profile = profile1)
                enrollment.course = course_added
                enrollment.isTeacher = True
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
            print("In")
            profile = mod.Profile.objects.get(user = request.user)
            if mod.Courses.objects.filter(access_code = form.cleaned_data.get('access_code')):
                course = mod.Courses.objects.filter(access_code = form.cleaned_data.get('access_code')).first()
                print('course',course.course_name,form.cleaned_data.get('master_code'),form.cleaned_data.get('assistant_code'))
                if mod.Enrollment.objects.filter(profile = profile , course= course):
                    print("Already exists, checking for teacher/assistant role")
                    enroll = mod.Enrollment.objects.get(profile = profile , course = course)
                    if(course.master_code == form.cleaned_data.get('master_code')):
                        enroll.isTeacher = True
                        enroll.save()
                    elif(course.assistant_code == form.cleaned_data.get('assistant_code')):
                        enroll.isAssistant = True
                        enroll.save()

                else:
                    enroll = mod.Enrollment(profile = profile , course = course)
                    print(course.master_code,course.assistant_code)
                    if(course.master_code == form.cleaned_data.get('master_code')):
                        enroll.isTeacher = True
                        print('enrolling as teacher')
                        enroll.save()
                    elif(course.assistant_code == form.cleaned_data.get('assistant_code')):
                        enroll.isAssistant = True
                        print('enrolling as assistant')
                        print(course.assistant_grading_privilege)
                        enroll.save()
                    else:
                        enroll.save()
                        for assignment in mod.Assignments.objects.filter(course = course):
                            x = mod.AssignmentCompleted(assignment = assignment , enrollment = enroll)
                            x.save()
                print('Added to course successfully')
            else:
                print('No course exists with access code: ', form.cleaned_data.get('access_code'))
        return redirect('dashboard', permanent = True)
    else:
        form = forms.CourseEnrollForm()
        return render(request , 'course_access.html',{'form': form})

def send_email( subject, message, email_from, recipient_list, html_message ):
    try:
        if html_message:
            send_mail( subject, message, email_from, recipient_list, html_message=html_message ) 
        else :
            send_mail( subject, message, email_from, recipient_list ) 
        print('success', recipient_list)
    except :
        print('Email failed')

def course_email(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile=mod.Profile.objects.get(user = request.user), course=mod.Courses.objects.get(course_name = course_name))
    course = mod.Courses.objects.get(course_name = course_name)
    if request.method == 'POST':
        form = forms.CourseEmailForm(request.POST)
        if form.is_valid():
            if enrollment.isTeacher or (enrollment.isAssistant and course.assistant_adding_privilege) :
                course = mod.Courses.objects.get(course_name=course_name)
                email_list = [s.strip() for s in form.cleaned_data.get('email_list').split(",")]
                message = 'Hi. This is an email giving you access to course '+course_name+'. Your access code is : ' + course.access_code
                if form.cleaned_data.get('assistant_email'):
                    message = 'Hi. This is an email giving you access to course '+course_name+'. Your access code is : ' + course.access_code + '. Your assistant code is : ' + course.assistant_code
                if form.cleaned_data.get('master_email'):
                    message = 'Hi. This is an email giving you access to course '+course_name+'. Your access code is : ' + course.access_code + '. Your master code is : ' + course.master_code
                subject = 'Course access code for course '+course_name
                recipient_list = email_list
                t1 = threading.Thread(target=send_email, args=(subject, message, email_from, recipient_list, None,  ))  
                t1.start()         
        return redirect('dashboard', permanent = True)
    else:
        if enrollment.isTeacher or (enrollment.isAssistant and course.assistant_adding_privilege) :
            form = forms.CourseEmailForm()
            return render(request , 'course_email.html',{'form': form})   
        else:
            return redirect('dashboard', permanent = True)

def create_boxchart(data, ticks):
    imgdata = StringIO()
    imgdata.truncate(0)
    imgdata.seek(0)
    plt.boxplot(data)
    plt.xticks([i for i in range(1,len(ticks)+1)], ticks)
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    plt.clf()
    return data 

def course_stats(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile=mod.Profile.objects.get(user = request.user), course=mod.Courses.objects.get(course_name = course_name))
    course = course=mod.Courses.objects.get(course_name = course_name)
    assignment_stats_dict = {}
    assignment_names = []
    assignment_grades = []
    chart = ""
    
    for assignment in mod.Assignments.objects.filter(course = course):
        grades = []
        profile_set = set()
        for sub in mod.AssignmentFiles.objects.filter(assignment = assignment):
            if sub.profile not in profile_set:
                profile_set.add(sub.profile)
                if sub.grade != 'Not graded yet':
                    grades.append(float(sub.grade))
        # print(grades)
        assignment_names.append(assignment.name)
        assignment_grades.append(grades)
        assignment_stats_dict[assignment.name] = "Mean : " + str(np.mean(grades)) + " Std : " + str(np.std(grades))
        chart = create_boxchart(assignment_grades, assignment_names)
        # print(chart,'chart')
        # print(assignment_stats_dict)
    if enrollment.isTeacher or enrollment.isAssistant:
        return render(request, 'course_stats.html', {'course_name' : course_name, 'assignment_dict' : assignment_stats_dict, 'chart':chart})
    else:
         return render(request, 'course_stats.html', {'course_name' : course_name, 'assignment_dict' : assignment_stats_dict})


def announcements_create(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    course = mod.Courses.objects.get(course_name = course_name)
    # if not (enrollment.isTeacher or (enrollment.isAssistant and course.assistant_creation_privilege)) :
        # this means that student is present, or TA with less privileges
    #     return redirect('assignments', course_name = course_name,permanent=True)
    # print("In here")
    if request.method == 'POST':
        form = forms.AnnouncementCreationForm(request.POST)
        if form.is_valid():
            course1 = mod.Courses.objects.get(course_name = course_name)
            message = mod.Message(course=course1)
            message.content = markdown.markdown(form.cleaned_data.get('content'))
            message.time_of_last_edit = datetime.datetime.now()
            message.author = mod.Profile.objects.get(user = request.user)
            message.save()
            print("fine")
            return redirect('announcements', course_name = course_name,permanent=True)
    else:
        form = forms.AnnouncementCreationForm()
        return render(request,'announcements_new.html',{'form':form})


def announcements(request, course_name):
    announcement_dict = {}
    course = mod.Courses.objects.get(course_name = course_name)
    enrollment = mod.Enrollment.objects.get(profile = mod.Profile.objects.get(user= request.user), course = course_name)
    if enrollment.isTeacher or (enrollment.isAssistant):
        teacher = True
    else:
        teacher = False
    if(mod.Message.objects.filter(course=course)):
        for parent_post in mod.Message.objects.filter(course = course):
                current_message = (parent_post.content, parent_post.id)
                announcement_dict[current_message] = []
                for reply in mod.Replies.objects.filter(parent_message = parent_post):
                    announcement_dict[current_message].append(reply.content)
                    
    return render(request,'announcements.html', {'data' : announcement_dict, 'course' : course_name, 'teacher':teacher})

def announcements_reply(request, course_name, id):
    if request.method == 'POST':
        form = forms.ReplyCreationForm(request.POST)
        if form.is_valid():
            message = mod.Message.objects.get(id = id)
            reply = mod.Replies(parent_message = message)
            reply.content = markdown.markdown(form.cleaned_data.get('content'))
            reply.time_of_last_edit = datetime.datetime.now()
            reply.author = mod.Profile.objects.get(user = request.user)
            reply.course = message.course
            reply.save()
            print("fine")
            return redirect('announcements', course_name = course_name,permanent=True)
    else:
        form = forms.ReplyCreationForm()
        return render(request,'announcements_new.html',{'form':form})

def grades(request, course_name):
    enrollment = mod.Enrollment.objects.get(profile=mod.Profile.objects.get(user = request.user), course=mod.Courses.objects.get(course_name = course_name))
    course =mod.Courses.objects.get(course_name = course_name)
    grades = {}
    course_total=0
    warning=""
    # This calculation is for the student
    if not (enrollment.isTeacher or enrollment.isAssistant):
        for assignment in mod.Assignments.objects.filter(course = course):
            profile_set = set()
            for sub in mod.AssignmentFiles.objects.filter(assignment = assignment, profile = mod.Profile.objects.get(user = request.user)):
                if sub.profile not in profile_set:
                    profile_set.add(sub.profile)
                    if sub.grade != 'Not graded yet':
                        grades[assignment.name] = sub.marks
                        course_total+=sub.marks*assignment.weightage
        enrollment.marks = course_total
        if(enrollment.marks<course_total/2):
            warning = "You are Significantly below the class average"
    else:
        count=0
        for assignment in mod.Assignments.objects.filter(course = course):
            profile_set = set()
            for sub in mod.AssignmentFiles.objects.filter(assignment = assignment):
                if sub.profile not in profile_set:
                    profile_set.add(sub.profile)
                    if sub.grade != 'Not graded yet':
                        grades[assignment.name] += sub.marks
                        course_total+=sub.marks*assignment.weightage
                        count+=1
            grades[assignment.name]/=count
        course_total/=count
        enrollment.marks = course_total
        course.class_average = course_total

    print("joiefje")
    
    return render(request,'grades.html',{'grades':grades, 'course_name':course_name, 'course_total':course_total, 'warning':warning})


def message_list(request):
    profile1 = mod.Profile.objects.get(user = request.user)   
    if request.method == 'POST':
        form = forms.MessageSearchForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data.get('username')
            if not request.user==receiver:
                if mod.Profile.objects.filter(user = receiver) :
                    print("valid hi tha")
                    profile2 = mod.Profile.objects.get(user = receiver)
                    if not ( mod.Conversation.objects.filter(person1 = profile1, person2 = profile2) or mod.Conversation.objects.filter(person1 = profile2, person2 = profile1) ) :
                        conversation = mod.Conversation(person1 = profile1, person2 = profile2)
                        conversation.save()
    form = forms.MessageSearchForm()
    convo_list = []
    for convo in mod.Conversation.objects.filter(person1 = profile1):
        convo_list.append(convo.person2.user)
    for convo in mod.Conversation.objects.filter(person2 = profile1):
        convo_list.append(convo.person1.user)
    return render(request, 'message_list.html', {'form':form, 'list' : convo_list})


def chat_screen(request, person):
    profile1 = mod.Profile.objects.get(user = request.user)
    receiver_person = mod.Profile.objects.get(user = person )
    chat_list = []
    if request.method == 'POST':
        form = forms.AddChat(request.POST)
        if form.is_valid():
            chat_message = form.cleaned_data.get('chat_message')
            if mod.Conversation.objects.filter(person1 = profile1, person2 = receiver_person):
                conversation =  mod.Conversation.objects.get(person1 = profile1, person2 = receiver_person)
                if conversation.messages == None:
                    conversation.senders= []
                    conversation.times= []
                    conversation.messages = []
                conversation.senders.append(True)
                conversation.times.append(datetime.datetime.now())
                conversation.messages.append(chat_message)
                conversation.save()
                length = len(conversation.messages)
                for index in range(length):
                    chat_list.append((conversation.messages[index],conversation.senders[index]))
            elif mod.Conversation.objects.filter(person1 = receiver_person, person2 = profile1 ):
                conversation =  mod.Conversation.objects.get(person1 = receiver_person, person2 = profile1)
                if conversation.messages == None:
                    conversation.senders= []
                    conversation.times= []
                    conversation.messages = []
                conversation.senders.append(False)
                conversation.times.append(datetime.datetime.now())
                conversation.messages.append(chat_message)
                conversation.save()
                length = len(conversation.messages)
                for index in range(length):
                    chat_list.append((conversation.messages[index],conversation.senders[index]))
            else:
                print(chat_message)
    else:
        if mod.Conversation.objects.filter(person1 = profile1, person2 = receiver_person):
            conversation =  mod.Conversation.objects.get(person1 = profile1, person2 = receiver_person)
            if conversation.messages == None:
                conversation.senders= []
                conversation.times= []
                conversation.messages = []
            length = len(conversation.messages)
            for index in range(length):
                chat_list.append((conversation.messages[index],conversation.senders[index]))
        elif mod.Conversation.objects.filter(person1 = receiver_person, person2 = profile1 ):
            conversation =  mod.Conversation.objects.get(person1 = receiver_person, person2 = profile1)
            if conversation.messages == None:
                conversation.senders= []
                conversation.times= []
                conversation.messages = []        
            length = len(conversation.messages)
            for index in range(length):
                chat_list.append((conversation.messages[index],conversation.senders[index]))
    form = forms.AddChat()
    return render(request, 'chat_list.html', {'form':form, 'chat_list' : chat_list})


def profile(request):
    courses_list=[]
    try:
        profile = mod.Profile.objects.get(user = request.user)
        for course in profile.courses.all():
            courses_list.append(course.course_name)
    except Exception as e:
        print(e)
    return render(request,'profile.html', {'courses_list': courses_list})

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
    new_profile = mod.Profile(user = request.user, email_id=request.user.member.email_id)
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


def edit_profile(request):
    if request.method == 'POST':
        form = forms.EditProfile(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('email_id') != '':
                request.user.member.email_id = form.cleaned_data.get('email_id')
            if form.cleaned_data.get('institute_name') != '':
                request.user.member.institute_name = form.cleaned_data.get('institute_name')
            request.user.save()
        return redirect('profile', permanent = True) 
    else:
        form = forms.EditProfile()
#        form.email_id = request.user.member.email_id
#        form.institute_name = request.user.member.institute_name
#        form.fields['email_id'].initial = request.user.member.email_id
#        form.fields['institute_name'].initial = request.user.member.institute_name
        context = {'form': form}
        return render(request , 'settings.html', context) 










