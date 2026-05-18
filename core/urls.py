from django.urls import path
from . import views
urlpatterns = [
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient/list/', views.patient_list, name='patient_list'),
    path('patient/details/<int:id>/', views.patient_details, name='patient_details')
]
