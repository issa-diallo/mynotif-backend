from django.contrib import admin

from nurse.models import (
    Nurse,
    Patient,
    Prescription,
    StripeProduct,
    Subscription,
    UserOneSignalProfile,
)


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
        "email_doctor",
        "start_date",
        "end_date",
    )


@admin.register(UserOneSignalProfile)
class UserOneSignalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscription_id",
    )


@admin.register(StripeProduct)
class StripeProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product_id",
        "monthly_price_id",
        "annual_price_id",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_active",
    )
