from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.utils.translation import deactivate

# Create your models here.

# class Student_Course(models.Model):
#     pair = models.CharField(max_length=1000),
#     Student|Course
#     # to access a students courses, iterate through all the entries of this model.
#     models.

class Courses(models.Model):
    course_name = models.CharField(max_length=100, primary_key=True)
    course_info = models.CharField(max_length=1000, default="Course Info")
    access_code = models.CharField(max_length=32, default="12345678")
    master_code = models.CharField(max_length=32, default="12345678")

    class Meta:
        ordering = ('course_name', )

    def __str__(self):
        return self.course_name

class Profile(models.Model):
    user = models.CharField(max_length=100 , primary_key = True)
    courses =  models.ManyToManyField(Courses , through = 'Enrollment')
    class Meta:
        ordering = ('user', )

    def __str__(self):
        return self.user

class Enrollment(models.Model):
    profile = models.ForeignKey(Profile , on_delete = models.CASCADE)
    course = models.ForeignKey(Courses , on_delete = models.CASCADE)
    grade = models.CharField(max_length = 100, blank = True , null = True)
    isTeacher = models.BooleanField(default = False)
    class Meta:
        unique_together = [['profile' , 'course']]

class Assignments(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1200, blank=True, null=True)
    
class AssignmentFiles(models.Model):
    assignment = models.ForeignKey(Assignments, on_delete=CASCADE)
    file = models.FileField(upload_to="files/%Y/%m/%d")

# class Grades(models.Model):
#     user = models.ForeignKey(Profile, on_delete=CASCADE)
#     course = models.CharField(max_length=100)
#     quiz = models.CharField(max_length=100)
#     grade = models.CharField(max_length=100)
#     feedback = models.CharField(max_length=100)
#     file = models.FileField(upload_to='uploads/') #change the url

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user','course','quiz'], name='user_course_quiz_grades'),
#         ]