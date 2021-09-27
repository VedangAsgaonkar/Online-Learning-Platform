from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    email_id = models.EmailField(max_length=100)
    institute_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_member_signal(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)
    instance.member.save()