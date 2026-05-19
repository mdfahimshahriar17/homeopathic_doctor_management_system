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


class PrescriptionItemForm(forms.ModelForm):
    medicine_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    medicine_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search medicine from list...'
        })
    )

    custom_medicine_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'If not found, type medicine name here'
        }) 
    )

    class Meta:
        model = models.PrescriptionItem
        fields = ['potency', 'dosage', 'duration', 'instruction']

        widgets = {
            'potency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 30C / 200C'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 3 drops / 2 pills'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 7 days'
            }),
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Instruction'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        medicine_id = cleaned_data.get('medicine_id')
        custom_medicine_name = cleaned_data.get('custom_medicine_name')

        if not medicine_id and not custom_medicine_name:
            raise forms.ValidationError(
                "Select a medicine from list or write custom medicine name."
            )

        return cleaned_data