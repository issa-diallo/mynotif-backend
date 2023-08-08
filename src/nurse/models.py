from datetime import datetime

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


class Prescription(models.Model):
    prescribing_doctor = models.CharField(max_length=300, blank=False)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    photo_prescription = models.ImageField(upload_to="prescriptions")
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.carte_vitale)

    def is_valid(self):
        """Returns true if the prescription is still valid (e.g. hasn't expired)."""
        return self.start_date <= datetime.now().date() <= self.end_date
