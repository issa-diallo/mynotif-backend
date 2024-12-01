from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


def make_street_field():
    return models.CharField(max_length=30, blank=True, default="")


def make_zip_code_field():
    return models.CharField(max_length=5, blank=True, default="")


def make_city_field():
    return models.CharField(max_length=300, blank=True, default="")


def make_phone_field():
    return models.CharField(max_length=30, blank=True, default="")


class Patient(models.Model):
    firstname = models.CharField(max_length=30, blank=False)
    lastname = models.CharField(max_length=30, blank=False)
    street = make_street_field()
    zip_code = make_zip_code_field()
    city = make_city_field()
    phone = make_phone_field()
    birthday = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    health_card_number = models.CharField(
        max_length=15, blank=True, help_text="carte vitale"
    )
    ss_provider_code = models.CharField(
        max_length=9, blank=True, help_text="code d'organisme de rattachement"
    )

    def __str__(self):
        return str(self.firstname)


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    phone = make_phone_field()
    address = make_street_field()
    zip_code = make_zip_code_field()
    city = make_city_field()
    patients = models.ManyToManyField(Patient, blank=True)

    def __str__(self):
        return str(self.user)


class PrescriptionManager(models.Manager):
    DEFAULT_EXPIRING_SOON_DAYS = 7

    def expiring_soon(self, days=DEFAULT_EXPIRING_SOON_DAYS):
        today = datetime.now().date()
        expiring_soon_date = today + timedelta(days=days)
        return self.filter(end_date__lte=expiring_soon_date, end_date__gte=today)


class Prescription(models.Model):
    prescribing_doctor = models.CharField(max_length=300, blank=False)
    email_doctor = models.EmailField(blank=True, null=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    photo_prescription = models.ImageField(upload_to="prescriptions")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    objects = PrescriptionManager()

    def __str__(self):
        return f"Prescription: {self.prescribing_doctor}"

    def is_valid(self):
        """Returns true if the prescription is still valid (e.g. hasn't expired)."""
        return self.start_date <= datetime.now().date() <= self.end_date

    def expiring_soon(self, days=PrescriptionManager.DEFAULT_EXPIRING_SOON_DAYS):
        """Returns true if the prescription is expiring soon."""
        today = datetime.now().date()
        expiring_soon_date = today + timedelta(days=days)
        return self.end_date <= expiring_soon_date and self.end_date >= today


class UserOneSignalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription of {self.user.username}"


class StripeProduct(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    monthly_price_id = models.CharField(max_length=255)
    annual_price_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
