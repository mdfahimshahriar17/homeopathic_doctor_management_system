from django.shortcuts import render, redirect
from . import forms


def register_patient(request):
    if request.method == 'POST':
        form = forms.PatientForm(request.POST)
        patient = form.save(commit=False)
        patient.created_by = request.user  # link patient to the logged-in user
        patient.save()
        return redirect('register_patient')

    else:
        form = forms.PatientForm()

    return render(request, 'core/create_patient.html', {'form' : form})