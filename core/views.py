from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from . import models

def register_patient(request):
    if request.method == 'POST':
        form = forms.PatientForm(request.POST)
        patient = form.save(commit=False)
        patient.created_by = request.user  # link patient to the logged-in user
        patient.save()
        return redirect('register_patient')

    else:
        form = forms.PatientForm()

    return render(request, 'core/create_and_edit_patient.html', {'form' : form})


def patient_list(request):
    patients = models.Patient.objects.all()

    return render(request, 'core/patient_list.html', {'patients' : patients})



def patient_details(request, id):
    patient = get_object_or_404(models.Patient, id=id)
    return render(request, 'core/patien_details.html', {'patient' : patient})
