from django.contrib import admin
from . import models


admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.Visit)
admin.site.register(models.Medicine)
admin.site.register(models.PrescriptionItem)