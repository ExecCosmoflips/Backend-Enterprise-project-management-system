from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=20, unique=True)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='userprofile', null=True)
    access = models.IntegerField(default='0')
    license = models.IntegerField(default='0')
    name = models.CharField(max_length=10, null=True)
    gender = models.IntegerField(default='0')
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)


class Project(models.Model):

    department = models.ForeignKey(Department, related_name='project', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default='')
    content = models.CharField(max_length=500, default='')
    begin_time = models.DateField(default=timezone.now)
    end_time = models.DateField(default=timezone.now)
    staff = models.ManyToManyField(User, related_name='project', null=True)

    def __str__(self):
        return self.title


class StaffRequest(models.Model):
    project = models.ForeignKey(Project, related_name='project_request', on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    whether = models.IntegerField(default='0')

class StaffRequest(models.Model):
    project = models.ForeignKey(Project, related_name='project_request', on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_request')
    whether = models.IntegerField(default='0')


class FinancialModel(models.Model):
    name = models.CharField(max_length=30, default='')
    number = models.IntegerField(default='0')
    status = models.IntegerField(default='0')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_financial')


class Expend(models.Model):
    project = models.ForeignKey(Project, related_name='project_expend', on_delete=models.CASCADE)
    category = models.ForeignKey(FinancialModel, related_name='category', on_delete=models.PROTECT)
    title = models.CharField(max_length=30, default='')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend', null=True)
    time = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class ConfirmExpend(models.Model):
    project = models.ForeignKey(Project, related_name='project_confirm', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend', null=True)
    time = models.DateField(default=timezone.now)


class Receivable(models.Model):
    project = models.ForeignKey(Project, related_name='project_receivable', on_delete=models.CASCADE)
    category = models.ForeignKey(FinancialModel,on_delete=models.PROTECT)
    title = models.CharField(max_length=30, default='')
    number = models.IntegerField(blank=False)
    agreement = models.ImageField(upload_to='confirm-expend', null=True)
    time = models.DateField(default=timezone.now)


class Advance(models.Model):
    project = models.ForeignKey(Project, related_name='project_advance', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')
    number = models.IntegerField(default='0')
    agreement = models.ImageField(upload_to='confirm-expend', null=True)
    time = models.DateField(default=timezone.now)


class Income(models.Model):
    project = models.ForeignKey(Project, related_name='project_income', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default='')
    confirm_num = models.FloatField(default = '0')
    tax_rate = models.FloatField(blank = False)
    agreement = models.ImageField(upload_to='confirm-expend', null=True)
    time = models.DateField(default=timezone.now)


class Company(models.Model):
    name = models.CharField(max_length=50, default='计蒜客')
    logo = models.ImageField(upload_to='logo')
    time = models.DateField(default=timezone.now)


