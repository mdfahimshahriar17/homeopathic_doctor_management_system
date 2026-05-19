from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max #aggregate function to get max
from django.utils import timezone #for select time zone
from django.db.models import Q #For query in models
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

@login_required
def register_patient(request):
    if request.method == 'POST':
            form = forms.PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.created_by = request.user  # link patient to the logged-in user
                patient.save()
                return redirect('patient_details', id=patient.id)

    else:
        form = forms.PatientForm()

    return render(request, 'core/create_and_edit_patient.html', {'form' : form})

@login_required
def patient_list(request):
    patients = models.Patient.objects.all()

    return render(request, 'core/patient_list.html', {'patients' : patients})


@login_required
def patient_details(request, id):
    patient = get_object_or_404(models.Patient, id=id)
    today = timezone.localdate()

    today_appointment = models.Appointment.objects.filter(
        patient=patient,
        appointment_date__date=today
    ).exclude(status='Cancelled').first()
    return render(request, 'core/patien_details.html', {'patient' : patient, 'today_appointment':today_appointment})


@login_required
def edit_patient(request, id):
    patient = models.Patient.objects.get(id=id)
    form = forms.PatientForm(instance=patient) #patient previous data will show in form

    if request.method == 'POST':
        form = forms.PatientForm(request.POST, instance=patient) #captured the user request post
        if form.is_valid():
            form.save()
            return redirect('patient_details', id=patient.id)
    return render(request, 'core/create_and_edit_patient.html', {'form': form, 'update': True})


@login_required
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

@login_required
def create_appointment(request, id):

    today = timezone.localdate()

    # Old pending appointments auto cancelled
    models.Appointment.objects.filter(
        appointment_date__date__lt=today,
        status='Pending'
    ).update(status='Cancelled')

    patient = get_object_or_404(models.Patient, id=id)

    if request.method == 'POST':
        next_url = request.POST.get('next')

        # Check if this patient already has appointment today
        existing_appointment = models.Appointment.objects.filter(
            patient=patient,
            appointment_date__date=today
        ).exclude(status='Cancelled').first()

        if existing_appointment:
            if next_url:
                return redirect(next_url)
            return redirect('appointment_list')

        # Ajker last serial number ber korlam
        last_serial = models.Appointment.objects.filter(
            appointment_date__date=today
        ).aggregate(max_serial=Max('serial_num'))['max_serial']

        appointment = models.Appointment()
        appointment.patient = patient
        appointment.appointment_date = timezone.now()
        appointment.serial_num = (last_serial or 0) + 1
        appointment.status = 'Pending'
        appointment.created_by = request.user
        appointment.save()

        if next_url:
            return redirect(next_url)

        return redirect('appointment_list')

    return redirect('patient_search')


@login_required
def appointment_list(request):
    today = timezone.localdate()
    appointments = models.Appointment.objects.filter(appointment_date__date=today).order_by('serial_num')


    return render(request, 'core/appointment_list.html', {'appointments' : appointments})



@login_required
def create_visit(request, id):
    appointment = get_object_or_404(models.Appointment, id=id)
    
    # jodi ei appointment er visit already thake
    existing_visit = models.Visit.objects.filter(appointment=appointment).first()

    if existing_visit:
        return redirect('patient_details', id=appointment.patient.id)
    
    if appointment.status == 'Pending':
        appointment.status = 'In_Visit'
        appointment.save()

    if request.method == 'POST':
        form = forms.VisitForm(request.POST)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.appointment = appointment
            visit.patient = appointment.patient
            visit.created_by = request.user
            visit.save()

            return redirect('patient_details', id=appointment.patient.id)
        
    else:
        form = forms.VisitForm()
        
    return render(request, 'core/visit_form.html', {'form': form, 'appointment': appointment, 'patient': appointment.patient})



def create_medicine(request):
    if request.method == 'POST':
        form = forms.MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.created_by = request.user
            medicine.save()
            return redirect('medicine_details')
        
    else:
        form = forms.MedicineForm()

    return render(request, 'core/created_and_edit_medicine', {'form' : form})


def medicine_details(request, id):
    medicine = get_object_or_404(models.Medicine, id=id)
    return render (request, 'core/medicine_details.html')



def medicine_list(request):
    medicines = models.Medicine.objects.all()

    return render(request, 'core/medicine_list.html', {'medicines':medicines})
