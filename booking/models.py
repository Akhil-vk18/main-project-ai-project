from django.db import models
from disease.models import *
from user_app.models import *
# Create your models here.



class DutyTime(models.Model):
    doctor = models.ForeignKey(Register, on_delete=models.CASCADE,related_name='duty_times')
    morning_start = models.CharField(max_length=255,null=True)
    evening_start = models.CharField(max_length=255,null=True)


    
    
class Book_Dr(models.Model):
    dr_id = models.ForeignKey(Register, on_delete=models.CASCADE,null=True,related_name='+')
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
    booking_time = models.CharField(max_length=255,null=True)
    booking_date = models.CharField(max_length=255,null=True)
    details = models.TextField(max_length=255,null=True)
    c_status = models.CharField(max_length=255, null=True)
    f_status = models.CharField(max_length=255, null=True)


