from django.urls import path
from . import views
urlpatterns = [
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient/list/', views.patient_list, name='patient_list'),
    path('patient/details/<int:id>/', views.patient_details, name='patient_details'),
    path('edit/patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('create/appointment/', views.create_appointment, name='create_appointment'),
    path('patient/search/', views.patient_search, name='patient_search'),
    path('appointment/create/<int:id>/', views.create_appointment, name='create_appointment'),
    path('appointment/list', views.appointment_list, name='appointment_list'),
    path('visit/create/<int:id>/', views.create_visit, name='create_visit' ),

    #CRUD Medicine
    path('creat/medicine/', views.create_medicine, name='create_medicine'),
    path('medicine/details/<int:id>/', views.medicine_details, name='medicine_details'),
    path('edit/medicine/<int:id>/', views.medicine_edit, name='medicine_edit'),
    path('medicine/list/', views.medicine_list, name='medicine_list'),
    path('medicine/search/', views.medicine_search, name='medicine_search'),

    # Prescription Item
    path('prescription/create/<int:id>/', views.create_prescription, name='create_prescription'),
    path('ajax/medicine-search/', views.medicine_ajax_search, name='medicine_ajax_search'),
    path('fee/create/<int:id>/', views.create_fee, name='create_fee'),
    path('compounder/queue/', views.compounder_queue, name='compounder_queue'),
    path('compounder/complete/<int:id>/', views.complete_medicine_preparation, name='complete_medicine_preparation'),

    # Home View
    path('home/', views.home, name='home'),


    path('compounder/dashboard/', views.compounder_dashboard, name='compounder_dashboard'),
    path('compounder/prescription/<int:id>/', views.compounder_prescription_detail, name='compounder_prescription_detail'),
    path('compounder/complete/<int:id>/', views.complete_medicine_preparation, name='complete_medicine_preparation'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
]
