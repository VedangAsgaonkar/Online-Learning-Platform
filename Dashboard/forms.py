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