from django.contrib import admin

from nurse.models import Nurse, Patient, Prescription


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "zip_code", "phone", "address")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "firstname",
        "lastname",
        "city",
        "zip_code",
        "phone",
        "street",
        "health_card_number",
        "ss_provider_code",
        "birthday",
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "prescribing_doctor",
        "start_date",
        "end_date",
    )
