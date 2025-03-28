from django import forms 
from .models import * 
from django.forms import modelformset_factory

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['disease']
        widgets = {
            'disease': forms.TextInput(attrs={'class': 'form-control'})
        }
        
