from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
import os
from django.views.generic import *
from  django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from django.forms.models import inlineformset_factory
from treatment.forms import *
# Create your views here.
def add_disease(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES)
        # formset = SymptomsFormSet(request.POST, request.FILES, queryset=Symptoms.objects.none())

        if form.is_valid():
            disease = form.save()  # Save the disease instance
            
            messages.success(request,f'Disase saved successfully.',extra_tags='log')
            return redirect('/disease_list') 
        else:
            print("Disease Form Errors:", form.errors)
    else:
        form = DiseaseForm()
        
    return render(request, 'add_disease.html', {'form': form})




class DiseaseListView(ListView):
    model = Disease
    template_name = 'disease_list.html'   
    context_object_name = 'diseases'
    
from django.forms.models import inlineformset_factory

def edit_disease_view(request, pk):
    disease_id = get_object_or_404(Disease, id=pk)

    if request.method == 'POST':
        form = DiseaseForm(request.POST, instance=disease_id)
        if form.is_valid():
            form.save()
            return redirect('disease_list')
        else:
            print(form.errors)
    else:
        form = DiseaseForm(instance=disease_id)

    return render(request, 'edit_disease.html', {'form': form})

def delete_disease(request, id):
    disease = get_object_or_404(Disease, id=id)
    disease.delete()
    return redirect('/disease_list')

