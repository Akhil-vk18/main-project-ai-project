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
# Create your views here.

def add_treatment(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        formset = SymptomsFormSet(request.POST)  # Initialize the formset with POST data

        if form.is_valid() and formset.is_valid():
            treatment_name = form.cleaned_data['treatment_name']
            if Treatments.objects.filter(treatment_name__iexact=treatment_name, dr_id=request.user.id).exists():
                messages.error(request, 'A Treatment with this name already exists.')
                return render(request, 'add_treatment.html', {'form': form, 'formset': formset, 'title': 'Add Treatments'})
            else:
                treat = form.save(commit=False)
                treat.dr_id = Register.objects.get(id=request.user.id)
                treat.save()

                # Save each symptom linked to the treatment
                symptoms = formset.save(commit=False)
                for symptom in symptoms:
                    symptom.treatment = treat  # Assuming you have a ForeignKey in Symptoms for Treatment
                    symptom.save()

                messages.success(request, 'Treatment and Symptoms saved successfully.', extra_tags='log')
                return redirect('/treatment_list')
        else:
            print("Treatment Form Errors:", form.errors)
            print("Symptoms FormSet Errors:", formset.errors)
    else:
        form = TreatmentForm()
        formset = SymptomsFormSet(queryset=Symptoms.objects.none())  # Initialize with an empty formset

    return render(request, 'add_treatment.html', {'form': form, 'formset': formset, 'title': 'Add Treatments'})
class TreatmentList(ListView):
    model = Treatments
    template_name = 'treatment_list.html'
    context_object_name = 'treatment'

    def get_queryset(self):
        dr_id = self.request.user.id
        return Treatments.objects.filter(dr_id=dr_id).prefetch_related('symptoms')
    
    from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Treatments, Symptoms
from .forms import TreatmentForm, SymptomsFormSet
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from .forms import TreatmentForm, SymptomsForm
from .models import Treatments, Symptoms

class EditTreatmentView(UpdateView):
    model = Treatments
    form_class = TreatmentForm
    template_name = 'edit_treatment.html'

    def get_object(self, queryset=None):
        treatment_id = self.kwargs.get('id')
        return get_object_or_404(Treatments.objects.prefetch_related('symptoms'), id=treatment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SymptomsFormSet(
                self.request.POST,
                queryset=Symptoms.objects.filter(treatment=self.object),
            )
        else:
            context['formset'] = SymptomsFormSet(
                queryset=Symptoms.objects.filter(treatment=self.object),
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            # Save treatment
            self.object = form.save()

            # Save related symptoms
            instances = formset.save(commit=False)
            for instance in instances:
                instance.treatment = self.object
                instance.save()

            # Delete unchecked symptoms
            formset.save_m2m()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('treatment_list')

def delete_treatment(request, id):
    disease = get_object_or_404(Treatments, id=id)
    disease.delete()
    return redirect('/disease_list')

