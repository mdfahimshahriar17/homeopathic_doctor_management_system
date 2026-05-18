from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max #aggregate function to get max
from django.utils import timezone #for select time zone
from django.db.models import Q #For query in models
from . import forms
from . import models

def register_patient(request):
    if request.method == 'POST':
            form = forms.PatientForm(request.POST)
            if form.is_valid():
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


def edit_patient(request, id):
    patient = models.Patient.objects.get(id=id)
    form = forms.PatientForm(instance=patient) #patient previous data will show in form

    if request.method == 'POST':
        form = forms.PatientForm(request.POST, instance=patient) #captured the user request post
        if form.is_valid():
            form.save()
            return redirect('patient_details', id=patient.id)
    return render(request, 'core/create_and_edit_patient.html', {'form': form, 'update': True})


def patient_search(request):
    query = request.GET.get('q', '')
    patients = []

    if query:
        patients = models.Patient.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )

        if query.isdigit():
            patients = patients | models.Patient.objects.filter(id=query)

    return render(request, 'core/patient_search.html', {
        'query': query,
        'patients': patients,
    }

    )

def create_appointment(request, id):
    patient = get_object_or_404(models.Patient, id=id)
    
    if request.method == 'POST':
        today = timezone.localdate() #today date pick korlam
        

        #django result dey dictionary akare
        last_serial = models.Appointment.objects.filter(
            appointment_date__date = today
        ).aggregate(max_serial=Max('serial_num'))['max_serial'] #ajker date er last patient ta k ber korlam
        
        appointment = models.Appointment()
        appointment.patient = patient
        appointment.appointment_date = timezone.now()
        appointment.serial_num = (last_serial or 0) + 1 
        appointment.created_by = request.user
        appointment.save()
        return redirect('appointment_list') 
    
    return redirect('patien_search')


def appointment_list(request):
    today = timezone.localdate()
    appointments = models.Appointment.objects.filter(appointment_date__date=today).order_by('serial_num')


    return render(request, 'core/appointment_list.html', {'appointments' : appointments})
