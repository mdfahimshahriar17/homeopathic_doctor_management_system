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
