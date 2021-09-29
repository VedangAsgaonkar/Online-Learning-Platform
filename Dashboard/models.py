from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.deletion import CASCADE
# Create your models here.

# class Student_Course(models.Model):
#     pair = models.CharField(max_length=1000),
#     Student|Course
#     # to access a students courses, iterate through all the entries of this model.
#     models.

class Courses(models.Model):
    course_name = models.CharField(max_length=100)#, primary_key=True)
    class Meta:
        ordering = ('course_name', )

    def __str__(self):
        return self.course_name

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    courses =  models.ManyToManyField(Courses)
    # name = models.CharField(max_length=100)
    class Meta:
        ordering = ('user', )

    def __str__(self):
        return self.name

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