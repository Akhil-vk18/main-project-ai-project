from django.db import models
from disease.models import *
from user_app.models import *
# Create your models here.

class Treatments(models.Model):
    dr_id = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE,null=True)
    treatment_name = models.CharField(max_length=255)
    details = models.TextField(max_length=255)
    def __str__(self):
        return self.treatment_name
  
    
class Symptoms(models.Model):
    treatment = models.ForeignKey(Treatments, on_delete=models.CASCADE, related_name='symptoms', null=True)  # Added this line
    symptom = models.CharField(max_length=255)

    def __str__(self):
        return self.symptom
