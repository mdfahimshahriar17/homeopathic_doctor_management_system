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

]
