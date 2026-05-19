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
    path('visit/create/<int:id>/', views.create_visit, name='create_visit' )
]
