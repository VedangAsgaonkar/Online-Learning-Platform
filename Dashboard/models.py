from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.deletion import CASCADE
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    course = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','course'], name='user_course_pair_profile'),
        ]

class Grades(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    course = models.CharField(max_length=100)
    quiz = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    feedback = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/') #change the url

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','course'], name='user_course_pair_grades'),
        ]