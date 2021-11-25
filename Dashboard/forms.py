from django import forms
from django.db.models.fields import NullBooleanField

class AssignmentCreationForm(forms.Form):
    assignment_name = forms.CharField(label="Assignment Name", max_length=100)
    weightage = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea)
    deadline = forms.DateTimeField(label = "Set Deadline")

class ContentCreationForm(forms.Form):
    content_name = forms.CharField(label="Content Name", max_length=100)
    description = forms.CharField(widget=forms.Textarea)

class AssignmentSubmissionForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple' : True}))

class CourseCreationForm(forms.Form):
    course_name = forms.CharField(label="COURSE Name", max_length=100)
    course_info = forms.CharField(widget=forms.Textarea)
    access_code = forms.CharField(min_length=8, max_length=32)
    assistant_code = forms.CharField(min_length=8, max_length=32)
    assistant_can_grade_assignments = forms.BooleanField(required=False)
    assistant_can_create_assignment = forms.BooleanField(required=False)
    assistant_can_add_students = forms.BooleanField(required=False)
    master_code = forms.CharField(min_length=8, max_length=32)

class CourseEnrollForm(forms.Form):
    access_code = forms.CharField(min_length=8, max_length=32)
    master_code = forms.CharField(min_length=8, max_length=32, required=False)
    assistant_code = forms.CharField(min_length=8, max_length=32, required=False)

class CourseEmailForm(forms.Form):
    email_list = forms.CharField(widget=forms.Textarea)
    master_email = forms.BooleanField(required=False)
    assistant_email = forms.BooleanField(required=False)

class AssignmentFeedbackForm(forms.Form):
    feedback_file = forms.FileField(widget=forms.ClearableFileInput())

class EditProfile(forms.Form):
    institute_name = forms.CharField(max_length=100, required=False)
    email_id = forms.EmailField(max_length=100, required=False)


class AnnouncementCreationForm(forms.Form):
    content = forms.CharField(label="Message", max_length=1000)

class ReplyCreationForm(forms.Form):
    content = forms.CharField(label="Reply", max_length=1000)

class MessageSearchForm(forms.Form):
    username = forms.CharField(label="Enter Username", max_length=30)

class AddChat(forms.Form):
    chat_message = forms.CharField(label="Enter your Message", max_length=1000)

class GUIGrader(forms.Form):
    marks = forms.FloatField(required=True) 
    feedback = forms.CharField(required=False)
