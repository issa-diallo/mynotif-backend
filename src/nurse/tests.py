from datetime import date
from freezegun import freeze_time
import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from .models import Nurse, Patient, Prescription


@pytest.mark.django_db
class TestPatient:

    client = APIClient()

    url = reverse_lazy("patient-list")

    data = {
        "firstname": "John",
        "lastname": "Leen",
        "address": "3 place du cerdan",
        "zip_code": "95400",
        "city": "courdimanche",
        "phone": "0602015454",
    }

    def test_endpoint_patient(self):
        assert self.url == "/patient/"

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


@pytest.mark.django_db
class TestPrescription:

    client = APIClient()

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

    def test_endpoind_prescription(self):
        assert self.url == "/prescription/"

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


@pytest.mark.django_db
class TestNurse:

    client = APIClient()

    url = reverse_lazy("nurse-list")

    data = {
        "user": 1,
        "phone": "0134643232",
        "address": "3 rue de pontoise",
        "zip_code": "95300",
        "city": "Pontoise",
    }

    def test_endpoind_nurse(self):
        assert self.url == "/nurse/"

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


@pytest.mark.django_db
class TestUser:

    client = APIClient()

    url = reverse_lazy("user-list")

    data = {
        "username": "@Issa",
        "email": "issa_test@test.com",
        "password": "password123!@",
    }

    def test_endpoind_user(self):
        assert self.url == "/user/"

    @freeze_time("2021-08-03 07:45:25")
    def test_create_user(self):
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert response.data == {
            "id": 1,
            "password": "password123!@",
            "last_login": None,
            "is_superuser": False,
            "username": "@Issa",
            "first_name": "",
            "last_name": "",
            "email": "issa_test@test.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2021-08-03T07:45:25Z",
            "groups": [],
            "user_permissions": [],
        }

    @freeze_time("2021-08-03 07:45:25")
    def test_list_user(self):
        User.objects.create()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": 1,
                "password": "",
                "last_login": None,
                "is_superuser": False,
                "username": "",
                "first_name": "",
                "last_name": "",
                "email": "",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2021-08-03T07:45:25Z",
                "groups": [],
                "user_permissions": [],
            }
        ]

    @freeze_time("2021-08-03 07:45:25")
    def test_detail_user(self):
        User.objects.create()
        response = self.client.get(reverse_lazy("user-detail", kwargs={"pk": 1}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "password": "",
            "last_login": None,
            "is_superuser": False,
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2021-08-03T07:45:25Z",
            "groups": [],
            "user_permissions": [],
        }

    @freeze_time("2021-08-03 07:45:25")
    def test_update_user(self):
        User.objects.create(**self.data)
        response = self.client.put(
            reverse_lazy("user-detail", kwargs={"pk": 1}), self.data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "password": "password123!@",
            "last_login": None,
            "is_superuser": False,
            "username": "@Issa",
            "first_name": "",
            "last_name": "",
            "email": "issa_test@test.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2021-08-03T07:45:25Z",
            "groups": [],
            "user_permissions": [],
        }

    def test_delete_user(self):
        User.objects.create(**self.data)
        response = self.client.delete(reverse_lazy("user-detail", kwargs={"pk": 1}))
        assert User.objects.count() == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
