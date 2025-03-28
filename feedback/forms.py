from django import forms
from .models import *




class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_rating(self):
        # Allow null/empty ratings
        rating = self.cleaned_data.get('rating')
        if rating is None or rating == '':
            return None
        return rating
