from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=20, unique=True)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leader')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='department_user', null=True)
    access = models.IntegerField(default='0')
    license = models.IntegerField(default='0')
    name = models.CharField(max_length=10, null=True)
    gender = models.IntegerField(default='0')
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)


class Project(models.Model):
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default='')
    content = models.CharField(max_length=500, default='')
    begin_time = models.DateField(default=timezone.now)
    end_time = models.DateField(default=timezone.now)
    staff = models.ManyToManyField(User, related_name='staff', null=True)

    def __str__(self):
        return self.title

class StaffRequest(models.Model):
    project = models.ForeignKey(Project, related_name='project_request', on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    whether = models.IntegerField(default='0')


class Expend(models.Model):
    project = models.ForeignKey(Project, related_name='project_expend', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=30, default='')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend')

    def __str__(self):
        return self.title


class ConfirmExpend(models.Model):
    project = models.ForeignKey(Project, related_name='project_confirm', on_delete=models.CASCADE)
    category = models.ForeignKey(Expend, on_delete=models.CASCADE, related_name='category')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend')


class Receivable(models.Model):
    project = models.ForeignKey(Project, related_name='project_receivable', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=30, default='')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend')


class Advance(models.Model):
    project = models.ForeignKey(Project, related_name='project_advance', on_delete=models.CASCADE)
    receivable = models.ForeignKey(Receivable, related_name='receivable_advance', on_delete=models.CASCADE)
    number = models.IntegerField(default='0')
    agreement = models.ImageField(upload_to='confirm-expend')


class Income(models.Model):
    project = models.ForeignKey(Project, related_name='project_income', on_delete=models.CASCADE)
    receivable = models.ForeignKey(Receivable, related_name='receivable_income', on_delete=models.CASCADE)
    confirm_num = models.FloatField(default = '0')
    tax_rate = models.FloatField(blank = False)
    agreement = models.ImageField(upload_to='confirm-expend')


class FinancialModel(models.Model):
    name = models.CharField(max_length=30, default='')
    number = models.IntegerField(default='0')
    status = models.IntegerField(default='0')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_financial')