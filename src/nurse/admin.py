from django.contrib import admin

from nurse.models import Nurse, Patient, Prescription


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "zip_code", "phone", "address")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "city", "zip_code", "phone", "address")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "carte_vitale",
        "caisse_rattachement",
        "prescribing_doctor",
        "start_date",
        "end_date",
        "at_renew",
    )
