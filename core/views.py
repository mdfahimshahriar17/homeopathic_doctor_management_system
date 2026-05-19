from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Sum, Count #aggregate function
from django.utils import timezone #for select time zone
from django.db.models import Q #For query in models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse #For ajax
from django.utils.dateparse import parse_date
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

    histories = []
    visit_dates = []
    history_date = request.GET.get('history_date', '')

    if request.user.role == 'doctor':
        visit_dates = models.Visit.objects.filter(
            patient=patient
        ).dates(
            'created_at',
            'day',
            order='DESC'
        )

        visits = models.Visit.objects.filter(
            patient=patient
        ).select_related(
            'appointment',
            'created_by'
        ).order_by('-created_at')

        if history_date:
            visits = visits.filter(created_at__date=history_date)

        for visit in visits:
            try:
                prescription = visit.prescription
                items = prescription.items.all()
            except models.Prescription.DoesNotExist:
                prescription = None
                items = []

            histories.append({
                'visit': visit,
                'prescription': prescription,
                'items': items,
            })

    return render(request, 'core/patient_details.html', {
        'patient': patient,
        'today_appointment': today_appointment,
        'histories': histories,
        'visit_dates': visit_dates,
        'history_date': history_date,
    })


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
        return redirect('create_prescription', id=existing_visit.id)
    
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

        return redirect('create_prescription', id=visit.id)        
    else:
        form = forms.VisitForm()
        
    return render(request, 'core/visit_form.html', {'form': form, 'appointment': appointment, 'patient': appointment.patient})



# Medicine CRUD

@login_required
def create_medicine(request):
    if request.method == 'POST':
        form = forms.MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.created_by = request.user
            medicine.save()
            return redirect('medicine_details', medicine.id)
        
    else:
        form = forms.MedicineForm()

    return render(request, 'core/created_and_edit_medicine.html', {'form' : form})

@login_required
def medicine_details(request, id):
    medicine = get_object_or_404(models.Medicine, id=id)
    return render (request, 'core/medicine_details.html', {'medicine':medicine})


@login_required
def medicine_list(request):
    medicines = models.Medicine.objects.all()

    return render(request, 'core/medicine_list.html', {'medicines':medicines})

@login_required
def medicine_edit(request, id):
    medicine = get_object_or_404(models.Medicine, id=id)
    form = forms.MedicineForm(instance=medicine) #medicine previous data will show in form

    if request.method == 'POST':
        form = forms.MedicineForm(request.POST, instance=medicine) #captured the user request post
        if form.is_valid():
            form.save()
            return redirect('medicine_details', id=medicine.id)
    
    return render(request, 'core/created_and_edit_medicine.html', {'form':form})

@login_required
def medicine_search(request):
    query = request.GET.get('q', '')
    medicines = []

    if query:
        medicines = models.Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        if query.isdigit():
            medicines = medicines | models.Medicine.objects.filter(id=query)
    
    return render(request, 'core/medicine_search.html', {'query': query, 'medicines': medicines})


#for jason search
@login_required
def medicine_ajax_search(request):
    query = request.GET.get('q', '')

    medicines = models.Medicine.objects.filter(
        name__icontains = query,
        is_active=True
    )[:10]

    data = []

    for medicine in medicines:
        data.append({
            'id': medicine.id,
            'name': medicine.name,
        })

    return JsonResponse({'results':data})



@login_required
def create_prescription(request, id):
    visit = get_object_or_404(models.Visit, id=id)

    prescription, created = models.Prescription.objects.get_or_create(
        visit=visit,
        defaults={
            'patient': visit.patient,
            'appointment': visit.appointment,
            'created_by': request.user,
        }
    )

    if request.method == 'POST':
        form = forms.PrescriptionItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.prescription = prescription

            medicine_id = form.cleaned_data.get('medicine_id')
            custom_medicine_name = form.cleaned_data.get('custom_medicine_name')

            if medicine_id:
                medicine = get_object_or_404(
                    models.Medicine,
                    id=medicine_id,
                    is_active=True
                )
                item.medicine = medicine
                item.custom_medicine_name = None
            else:
                item.medicine = None
                item.custom_medicine_name = custom_medicine_name

            item.save()

            return redirect('create_prescription', id=visit.id)

    else:
        form = forms.PrescriptionItemForm()

    items = models.PrescriptionItem.objects.filter(
        prescription=prescription
    )

    return render(request, 'core/prescription_form.html', {
        'visit': visit,
        'patient': visit.patient,
        'prescription': prescription,
        'form': form,
        'items': items,
    })



@login_required
def create_fee(request, id):
    prescription = get_object_or_404(models.Prescription, id=id)

    existing_fee = models.Fee.objects.filter(prescription=prescription).first()

    if existing_fee:
        return redirect('compounder_queue')

    if request.method == 'POST':
        form = forms.FeeForm(request.POST)

        if form.is_valid():
            fee = form.save(commit=False)
            fee.prescription = prescription
            fee.visit = prescription.visit
            fee.patient = prescription.patient
            fee.appointment = prescription.appointment
            fee.created_by = request.user
            fee.save()

            return redirect('doctor_dashboard')

    else:
        form = forms.FeeForm()

    return render(request, 'core/fee_form.html', {
        'form': form,
        'prescription': prescription,
        'patient': prescription.patient,
        'visit': prescription.visit,
    })


@login_required
def compounder_queue(request):
    fees = models.Fee.objects.select_related(
        'patient', 'prescription', 'appointment'
    ).exclude(
        appointment__status='Completed'
    ).order_by('created_at')

    return render(request, 'core/compounder_queue.html', {
        'fees': fees
    })


@login_required
def complete_medicine_preparation(request, id):
    fee = get_object_or_404(models.Fee, id=id)

    if request.method == 'POST':
        appointment = fee.appointment
        appointment.status = 'Completed'
        appointment.save()

    return redirect('compounder_queue')



@login_required
def home(request):
    if request.user.role == 'compounder':
        return redirect('compounder_dashboard')

    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')

    elif request.user.role == 'receptionist':
        return redirect('receptionist_dashboard')

    return redirect('patient_search')

@login_required
def compounder_dashboard(request):
    today = timezone.localdate()

    pending_fees = models.Fee.objects.select_related(
        'patient',
        'prescription',
        'appointment'
    ).prefetch_related(
        'prescription__items__medicine'
    ).filter(
        is_paid=False
    ).exclude(
        appointment__status='Completed'
    ).order_by('created_at')

    completed_today_count = models.Fee.objects.filter(
        is_paid=True,
        paid_at__date=today
    ).count()

    today_cash = models.Fee.objects.filter(
        is_paid=True,
        paid_at__date=today
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    pending_count = pending_fees.count()

    return render(request, 'core/compounder_dashboard.html', {
        'pending_fees': pending_fees,
        'pending_count': pending_count,
        'completed_today_count': completed_today_count,
        'today_cash': today_cash,
    })

@login_required
def compounder_prescription_detail(request, id):
    fee = get_object_or_404(
        models.Fee.objects.select_related(
            'patient',
            'prescription',
            'appointment',
            'visit'
        ).prefetch_related(
            'prescription__items__medicine'
        ),
        id=id
    )

    items = fee.prescription.items.all()

    return render(request, 'core/compounder_prescription_detail.html', {
        'fee': fee,
        'patient': fee.patient,
        'prescription': fee.prescription,
        'items': items,
    })

@login_required
def complete_medicine_preparation(request, id):
    fee = get_object_or_404(models.Fee, id=id)

    if request.method == 'POST':
        fee.is_paid = True
        fee.paid_at = timezone.now()
        fee.collected_by = request.user
        fee.save()

        appointment = fee.appointment
        appointment.status = 'Completed'
        appointment.save()

        return redirect('compounder_dashboard')

    return redirect('compounder_dashboard')



@login_required
def doctor_dashboard(request):
    today = timezone.localdate()

    selected_date_str = request.GET.get('date')
    selected_date = parse_date(selected_date_str) if selected_date_str else today

    if selected_date is None:
        selected_date = today

    # Appointment status auto update for old pending appointments
    models.Appointment.objects.filter(
        appointment_date__date__lt=today,
        status='Pending'
    ).update(status='Cancelled')

    total_patients = models.Patient.objects.count()

    today_appointments = models.Appointment.objects.filter(
        appointment_date__date=today
    ).select_related('patient').order_by('serial_num')

    total_today_appointments = today_appointments.count()
    pending_appointments = today_appointments.filter(status='Pending').count()
    in_visit_appointments = today_appointments.filter(status='In Visit').count()
    completed_appointments = today_appointments.filter(status='Completed').count()
    cancelled_appointments = today_appointments.filter(status='Cancelled').count()

    lifetime_earning = models.Fee.objects.filter(
        is_paid=True
    ).aggregate(total=Sum('amount'))['total'] or 0

    today_earning = models.Fee.objects.filter(
        is_paid=True,
        paid_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    selected_date_earning = models.Fee.objects.filter(
        is_paid=True,
        paid_at__date=selected_date
    ).aggregate(total=Sum('amount'))['total'] or 0

    today_medicine_count = models.PrescriptionItem.objects.filter(
        prescription__fee__is_paid=True,
        prescription__fee__paid_at__date=today
    ).count()

    selected_date_medicine_count = models.PrescriptionItem.objects.filter(
        prescription__fee__is_paid=True,
        prescription__fee__paid_at__date=selected_date
    ).count()

    not_in_list_medicines_today = models.PrescriptionItem.objects.filter(
        prescription__fee__is_paid=True,
        prescription__fee__paid_at__date=today,
        medicine__isnull=True
    ).exclude(
        custom_medicine_name__isnull=True
    ).exclude(
        custom_medicine_name=''
    ).order_by('-id')[:10]

    zero_fee_prescription_count = models.Fee.objects.filter(
    is_paid=True,
    paid_at__date=today,
    amount=0
    ).count()

    selected_date_zero_fee_prescription_count = models.Fee.objects.filter(
    is_paid=True,
    paid_at__date=selected_date,
    amount=0
    ).count()

    return render(request, 'core/doctor_dashboard.html', {
        'today': today,
        'selected_date': selected_date,

        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'total_today_appointments': total_today_appointments,

        'pending_appointments': pending_appointments,
        'in_visit_appointments': in_visit_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,

        'lifetime_earning': lifetime_earning,
        'today_earning': today_earning,
        'selected_date_earning': selected_date_earning,

        'today_medicine_count': today_medicine_count,
        'selected_date_medicine_count': selected_date_medicine_count,

        'not_in_list_medicines_today': not_in_list_medicines_today,
        
        'zero_fee_prescription_count': zero_fee_prescription_count,

        'selected_date_zero_fee_prescription_count': selected_date_zero_fee_prescription_count,
    })



@login_required
def receptionist_dashboard(request):
    today = timezone.localdate()

    # Old pending appointments auto cancelled
    models.Appointment.objects.filter(
        appointment_date__date__lt=today,
        status='Pending'
    ).update(status='Cancelled')

    today_appointments = models.Appointment.objects.filter(
        appointment_date__date=today
    ).select_related('patient').order_by('serial_num')

    total_today_appointments = today_appointments.count()
    pending_appointments = today_appointments.filter(status='Pending').count()
    in_visit_appointments = today_appointments.filter(status='In Visit').count()
    completed_appointments = today_appointments.filter(status='Completed').count()
    cancelled_appointments = today_appointments.filter(status='Cancelled').count()

    return render(request, 'core/receptionist_dashboard.html', {
        'today': today,
        'today_appointments': today_appointments,
        'total_today_appointments': total_today_appointments,
        'pending_appointments': pending_appointments,
        'in_visit_appointments': in_visit_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
    })


