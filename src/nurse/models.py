from django.contrib.auth.models import User
from django.db import models

def make_phone_field():
    return models.CharField(max_length=30, blank=False)

class Patient(models.Model):
    firstname = models.CharField(max_length=30, blank=False)
    lastname = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=300, blank=False)
    zip_code = models.CharField(blank=False, max_length=5)
    city = models.CharField(max_length=300, blank=False)
    phone = make_phone_field()


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    phone = make_phone_field()
    address = models.CharField(max_length=300, blank=False)
    zip_code = models.CharField(max_length=5, blank=False)
    city = models.CharField(max_length=300, blank=False)
    patients = models.ManyToManyField(Patient, blank=True)

    class Meta:
        verbose_name = "Infirmiere"

    def __str__(self):
        return self.user


class Prescription(models.Model):
    carte_vitale = models.IntegerField()
    caisse_rattachement = models.IntegerField()
    prescribing_doctor = models.CharField(max_length=300, blank=False)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    at_renew = models.BooleanField(blank=False)
    photo_prescription = models.CharField(max_length=300, blank=False)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
