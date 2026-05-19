from django import forms
from . import models


class PatientForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        exclude = ['created_by', 'created_at', 'updated_at']

        labels = {
            'name': "Full Name",
            'gender': "Select Gender",
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['patient']
        labels = {
            'patient': 'Select Patient'
        }


class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['symptoms', 'notes']

        widgets = {
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'notes': forms.Textarea(attrs={'class':'form-control', 'rows':3})
        }



class MedicineForm(forms.ModelForm):
    class Meta:
        model = models.Medicine
        fields = ['name', 'description', 'is_active']
        labels = {'name' : "Medicine Name"}