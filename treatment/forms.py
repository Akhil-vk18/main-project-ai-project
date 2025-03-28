from django import forms 
from .models import * 
from django.forms import modelformset_factory
from disease.models import *


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatments
        fields=['disease','treatment_name','details']
        widgets = {
            'symptom': forms.TextInput(attrs={'class': 'form-control'})
        }


class SymptomsForm(forms.ModelForm):
    class Meta:
        model = Symptoms
        fields=['symptom']
        widgets = {
            'symptom': forms.TextInput(attrs={'class': 'form-control'})
        }

SymptomsFormSet = modelformset_factory(Symptoms, form=SymptomsForm, extra=0, can_delete=True)
