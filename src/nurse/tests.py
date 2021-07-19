from datetime import date

from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Nurse, Patient, Prescription


class PatientTests(APITestCase):
    url = reverse_lazy("patient-list")

    data = {
        "firstname": "John",
        "lastname": "Leen",
        "address": "3 place du cerdan",
        "zip_code": "95400",
        "city": "courdimanche",
        "phone": "0602015454",
    }

    def test_create_patient(self):
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Patient.objects.count() == 1
        patient = Patient.objects.get(phone="0602015454")
        assert patient.firstname == "John"
        assert patient.lastname == "Leen"
        assert patient.address == "3 place du cerdan"
        assert patient.zip_code == "95400"
        assert patient.city == "courdimanche"

    def test_patient_list(self):
        Patient.objects.create(**self.data)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": 1,
                "firstname": "John",
                "lastname": "Leen",
                "address": "3 place du cerdan",
                "zip_code": "95400",
                "city": "courdimanche",
                "phone": "0602015454",
            }
        ]

    def test_patient_detail(self):
        Patient.objects.create(**self.data)
        response = self.client.get(reverse_lazy("patient-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "firstname": "John",
            "lastname": "Leen",
            "address": "3 place du cerdan",
            "zip_code": "95400",
            "city": "courdimanche",
            "phone": "0602015454",
        }

    def test_patient_delete(self):
        Patient.objects.create(**self.data)
        response = self.client.delete(reverse_lazy("patient-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert Patient.objects.count() == 0


class PrescriptionTests(APITestCase):

    url = reverse_lazy("prescription-list")

    data = {
        "carte_vitale": "12345678910",
        "caisse_rattachement": "12345678910",
        "prescribing_doctor": "Dr Leen",
        "start_date": "2022-07-15",
        "end_date": "2022-07-31",
        "at_renew": 1,
        "photo_prescription": "path_image",
    }

    my_start_date = date(2022, 7, 15)
    my_end_date = date(2022, 7, 31)

    def test_create_prescription(self):
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Prescription.objects.count() == 1
        prescription = Prescription.objects.get(carte_vitale="12345678910")
        assert prescription.caisse_rattachement == "12345678910"
        assert prescription.prescribing_doctor == "Dr Leen"
        assert prescription.start_date == self.my_start_date
        assert prescription.end_date == self.my_end_date
        assert prescription.at_renew == 1
        assert prescription.photo_prescription == "path_image"

    def test_prescription_list(self):
        Prescription.objects.create(**self.data)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": 1,
                "carte_vitale": "12345678910",
                "caisse_rattachement": "12345678910",
                "prescribing_doctor": "Dr Leen",
                "start_date": "2022-07-15",
                "end_date": "2022-07-31",
                "at_renew": 1,
                "photo_prescription": "path_image",
                "patient": None,
            }
        ]

    def test_prescription_detail(self):
        Prescription.objects.create(**self.data)
        response = self.client.get(
            reverse_lazy("prescription-detail", kwargs={"pk": 1})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "carte_vitale": "12345678910",
            "caisse_rattachement": "12345678910",
            "prescribing_doctor": "Dr Leen",
            "start_date": "2022-07-15",
            "end_date": "2022-07-31",
            "at_renew": 1,
            "photo_prescription": "path_image",
            "patient": None,
        }

    def test_prescription_delete(self):
        Prescription.objects.create(**self.data)
        response = self.client.delete(
            reverse_lazy("prescription-detail", kwargs={"pk": 1})
        )
        assert Prescription.objects.count() == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None


class NurseTests(APITestCase):
    url = reverse_lazy("nurse-list")

    data = {
        "user": 1,
        "phone": "0134643232",
        "address": "3 rue de pontoise",
        "zip_code": "95300",
        "city": "Pontoise",
    }

    def test_create_nurse(self):
        user = User.objects.create()
        response = self.client.post(self.url, self.data, format="json")
        assert response.data == {
            **self.data,
            **{
                "id": 1,
                "patients": [],
            },
        }
        assert response.status_code == status.HTTP_201_CREATED
        nurse = Nurse.objects.get(phone="0134643232")
        assert Nurse.objects.count() == 1
        assert nurse.user == user
        assert nurse.address == "3 rue de pontoise"
        assert nurse.zip_code == "95300"
        assert nurse.city == "Pontoise"

    def test_nurse_list(self):
        user = User.objects.create()
        Nurse.objects.create(
            user=user,
            phone="0134643232",
            address="3 rue de pontoise",
            zip_code="95300",
            city="Pontoise",
        )
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": 1,
                "user": 1,
                "patients": [],
                "phone": "0134643232",
                "address": "3 rue de pontoise",
                "zip_code": "95300",
                "city": "Pontoise",
            }
        ]

    def test_nurse_detail(self):
        user = User.objects.create()
        Nurse.objects.create(
            user=user,
            phone="0134643232",
            address="3 rue de pontoise",
            zip_code="95300",
            city="Pontoise",
        )
        response = self.client.get(reverse_lazy("nurse-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "user": 1,
            "patients": [],
            "phone": "0134643232",
            "address": "3 rue de pontoise",
            "zip_code": "95300",
            "city": "Pontoise",
        }
