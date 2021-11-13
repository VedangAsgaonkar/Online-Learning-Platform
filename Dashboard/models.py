from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.utils.translation import deactivate
import datetime
class Courses(models.Model):
    course_name = models.CharField(max_length=100, primary_key=True)
    course_info = models.CharField(max_length=1000, default="Course Info")
    access_code = models.CharField(max_length=32, default="12345678")
    master_code = models.CharField(max_length=32, default="12345678")
    assistant_code = models.CharField(max_length=32, default="12345678")
    assistant_grading_privilege = models.BooleanField(default = False)
    assistant_creation_privilege = models.BooleanField(default = False)
    assistant_adding_privilege = models.BooleanField(default = False)

    class Meta:
        ordering = ('course_name', )

    def __str__(self):
        return self.course_name

class Profile(models.Model):
    user = models.CharField(max_length=100 , primary_key = True)
    email_id = models.EmailField(max_length=100, null=True)
    courses =  models.ManyToManyField(Courses , through = 'Enrollment')
    class Meta:
        ordering = ('user', )

    def __str__(self):
        return self.user

class Enrollment(models.Model):
    profile = models.ForeignKey(Profile , on_delete = models.CASCADE)
    course = models.ForeignKey(Courses , on_delete = models.CASCADE)
    grade = models.CharField(max_length = 100, blank = True , null = True)
    marks = models.FloatField(default=0, null=True)
    isTeacher = models.BooleanField(default = False)
    isAssistant = models.BooleanField(default=False)
    class Meta:
        unique_together = [['profile' , 'course']]

class Assignments(models.Model):
    course = models.ForeignKey(Courses , on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1200, blank=True, null=True)
    deadline = models.DateTimeField(blank = True, null = True)
    weightage = models.FloatField(default = 0)

def getFileName(instance, filename):
    return 'files/'+instance.file_name+'/'+filename

class AssignmentFiles(models.Model):
    assignment = models.ForeignKey(Assignments, on_delete=CASCADE)
    file_name = models.CharField(max_length=100, default="files/vedang")
    file = models.FileField(upload_to=getFileName)
    profile = models.ForeignKey(Profile , null = True, on_delete=CASCADE)
    feedback = models.CharField(max_length = 100, default="No feedback yet", null=True, blank = True)
    grade = models.CharField(max_length = 100,default="Not graded yet", null=True, blank = True)
    marks = models.FloatField(default =0)

class AssignmentCompleted(models.Model):
	enrollment = models.ForeignKey(Enrollment, on_delete=CASCADE)	
	assignment = models.ForeignKey(Assignments, on_delete=CASCADE)
	isCompleted = models.BooleanField(default=False)







