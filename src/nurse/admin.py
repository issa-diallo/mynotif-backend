from django.contrib import admin
from nurse.models import Nurse, Patient, Prescription

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    pass

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass

