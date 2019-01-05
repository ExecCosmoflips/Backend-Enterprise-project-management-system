from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=20, unique=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE)
    leader = models.ForeignKey(User,related_name='user', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default='')
    content = models.CharField(max_length=500, default='')
    begin_time = models.DateField(null=False, default=timezone.now)
    end_time = models.DateField(null=False, default=timezone.now)
