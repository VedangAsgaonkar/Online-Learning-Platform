from django import forms

class AssignmentCreationForm(forms.Form):
    assignment_name = forms.CharField(label="Assignment Name", max_length=100)
    description = forms.CharField(widget=forms.Textarea)

class AssignmentSubmissionForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple' : True}))

class CourseCreationForm(forms.Form):
    course_name = forms.CharField(label="COURSE Name", max_length=100)
    course_info = forms.CharField(widget=forms.Textarea)
    access_code = forms.CharField(min_length=8, max_length=32)
    master_code = forms.CharField(min_length=8, max_length=32)

class CourseEnrollForm(forms.Form):
    access_code = forms.CharField(min_length=8, max_length=32)
    master_code = forms.CharField(min_length=8, max_length=32, required=False)

class CourseEmailForm(forms.Form):
    email_list = forms.CharField(widget=forms.Textarea)
    master_email = forms.BooleanField()

class AssignmentFeedbackForm(forms.Form):
    feedback_file = forms.FileField(widget=forms.ClearableFileInput())

class EditProfile(forms.Form):
    institute_name = forms.CharField(max_length=100, required=False)
    email_id = forms.EmailField(max_length=100, required=False)


