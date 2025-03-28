from django import forms
from django.forms import modelformset_factory
from .models import *

# Morning time choices (up to 12:00 PM)
# MORNING_TIME_CHOICES = [
#     ('6:00 AM - 7:00 AM', '6:00 AM - 7:00 AM'),
#     ('7:00 AM - 8:00 AM', '7:00 AM - 8:00 AM'),
#     ('8:00 AM - 9:00 AM', '8:00 AM - 9:00 AM'),
#     ('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'),
#     ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
#     ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
#     ('12:00 PM - 1:00 PM', '12:00 PM - 1:00 PM'),
#     ('no-op', 'no-op'),
# ]

# # Evening time choices (from 3:00 PM to 12:00 AM)
# EVENING_TIME_CHOICES = [
#     ('3:00 PM - 4:00 PM', '3:00 PM - 4:00 PM'),
#     ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM'),
#     ('5:00 PM - 6:00 PM', '5:00 PM - 6:00 PM'),
#     ('6:00 PM - 7:00 PM', '6:00 PM - 7:00 PM'),
#     ('7:00 PM - 8:00 PM', '7:00 PM - 8:00 PM'),
#     ('8:00 PM - 9:00 PM', '8:00 PM - 9:00 PM'),
#     ('9:00 PM - 10:00 PM', '9:00 PM - 10:00 PM'),
#     ('10:00 PM - 11:00 PM', '10:00 PM - 11:00 PM'),
#     ('11:00 PM - 12:00 AM', '11:00 PM - 12:00 AM'),
#     ('no-op', 'no-op'),
# ]

class OperatingTimeForm(forms.ModelForm):
    class Meta:
        model = DutyTime
        fields = ['morning_start', 'evening_start']
        widgets = {
            'morning_start': forms.TextInput(),
            'evening_start': forms.TextInput(),
        }

# Creating a formset for DutyTime, allowing 7 entries (one for each day of the week)
OperatingTimeFormSet = modelformset_factory(DutyTime, form=OperatingTimeForm, extra=7)


