from django import forms

class AssignmentCreationForm(forms.Form):
    assignment_name = forms.CharField(label="Assignment Name", max_length=100)
    description = forms.CharField(widget=forms.Textarea)

class AssignmentSubmissionForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple' : True}))