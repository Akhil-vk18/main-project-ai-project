from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from disease.models import *

class Register(AbstractUser):
    usertype = models.IntegerField(default=0)
    phone = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default='', null=True)
    place = models.CharField(max_length=200,  default='', null=True)
    reject_reason = models.TextField(default='', null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    experience = models.CharField(max_length=200, default='')
    qualification = models.CharField(max_length=50,default='')
    specialization = models.CharField(max_length=50,default='')
    location = models.CharField(max_length=200,  default='', null=True)
    lat = models.FloatField(max_length=200, null=True)
    long = models.FloatField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    
