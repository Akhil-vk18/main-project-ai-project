from django.db import models
# Create your models here.
class Disease(models.Model):
    disease = models.CharField(max_length=200)

    def __str__(self):
        return self.disease
    
