from datetime import date
from freezegun import freeze_time
import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from .models import Nurse, Patient, Prescription


def authenticate(client, username, password):
    """Creates a user and authenticates it via token."""
    username_kw = {"username": username}
    password_kw = {"password": password}
    credentials = {**username_kw, **password_kw}
    user = User.objects.create(**username_kw)
    user.set_password(credentials["password"])
    user.save()
    # voids previous credentials to avoid "Invalid token" errors
    client.credentials()
    response = client.post(
        reverse_lazy("api_token_auth"), {**credentials}, format="json"
    )
    token = response.data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


prescription_data = {
    "carte_vitale": "12345678910",
    "caisse_rattachement": "12345678910",
    "prescribing_doctor": "Dr Leen",
    "start_date": "2022-07-15",
    "end_date": "2022-07-31",
    "at_renew": 1,
    "photo_prescription": "path_image",
}


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

    username = "username1"
    password = "password1"

    def setup_method(self, method):
        """Creates a user and authenticates it via token."""
        authenticate(self.client, self.username, self.password)

    def teardown_method(self, method):
        """Invalidate credentials."""
        self.client.credentials()

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

    # TODO: this should be authenticated users only
    @freeze_time("2022-08-11")
    def test_patient_list(self):
        patient = Patient.objects.create(**self.data)
        # note that we create 3 prescriptions, but only the last two should show up
        Prescription.objects.create(**{**prescription_data, **{"patient": patient}})
        Prescription.objects.create(
            **{
                **prescription_data,
                **{
                    "patient": patient,
                    "start_date": "2022-08-01",
                    "end_date": "2022-08-10",
                },
            }
        )
        Prescription.objects.create(
            **{
                **prescription_data,
                **{
                    "patient": patient,
                    "start_date": "2022-08-10",
                    "end_date": "2022-08-20",
                },
            }
        )
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
                "prescriptions": [
                    {
                        "id": 3,
                        "patient": 1,
                        "carte_vitale": "12345678910",
                        "caisse_rattachement": "12345678910",
                        "prescribing_doctor": "Dr Leen",
                        "start_date": "2022-08-10",
                        "end_date": "2022-08-20",
                        "at_renew": 1,
                        "photo_prescription": "path_image",
                        "is_valid": True,
                    },
                    {
                        "id": 2,
                        "patient": 1,
                        "carte_vitale": "12345678910",
                        "caisse_rattachement": "12345678910",
                        "prescribing_doctor": "Dr Leen",
                        "start_date": "2022-08-01",
                        "end_date": "2022-08-10",
                        "at_renew": 1,
                        "photo_prescription": "path_image",
                        "is_valid": False,
                    },
                ],
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
            "prescriptions": [],
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

    data = prescription_data
    username = "username1"
    password = "password1"

    def setup_method(self, method):
        """Creates a user and authenticates it via token."""
        authenticate(self.client, self.username, self.password)

    def teardown_method(self, method):
        """Invalidate credentials."""
        self.client.credentials()

    my_start_date = date(2022, 7, 15)
    my_end_date = date(2022, 7, 31)

    def test_endpoint(self):
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

    @freeze_time("2022-08-11")
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
                "is_valid": False,
            }
        ]

    @freeze_time("2022-07-20")
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
            "is_valid": True,
        }

    # TODO:
    # makes sure we can only delete the prescription associated to the
    # authenticated user
    def test_prescription_delete(self):
        Prescription.objects.create(**self.data)
        response = self.client.delete(
            reverse_lazy("prescription-detail", kwargs={"pk": 1})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert Prescription.objects.count() == 0


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

    username = "username1"
    password = "password1"

    def setup_method(self, method):
        """Creates a user and authenticates it via token."""
        authenticate(self.client, self.username, self.password)

    def teardown_method(self, method):
        """Invalidate credentials."""
        self.client.credentials()

    def test_endpoint(self):
        assert self.url == "/nurse/"

    def test_create_nurse(self):
        user = User.objects.get()
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
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
        user = User.objects.get()
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
        user = User.objects.get()
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

    def test_endpoint(self):
        assert self.url == "/user/"

    def test_create_user(self):
        """The user creation is via another a different endpoint (/account/register)."""
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # it should be no way to create user via this endpoint
        # even being authenticated
        authenticate(self.client, self.data["username"], self.data["password"])
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_list_user(self):
        authenticate(self.client, self.data["username"], self.data["password"])
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": 1,
                "username": self.data["username"],
                "first_name": "",
                "last_name": "",
                "email": "",
            }
        ]

    def test_detail_user(self):
        authenticate(self.client, self.data["username"], self.data["password"])
        response = self.client.get(reverse_lazy("user-detail", kwargs={"pk": None}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "username": self.data["username"],
            "first_name": "",
            "last_name": "",
            "email": "",
        }

    @pytest.mark.parametrize(
        "action",
        [
            # get
            (lambda client, path, data=None, format=None: client.get(path)),
            # put
            (
                lambda client, path, data=None, format=None: client.put(
                    path, data, format
                )
            ),
            # patch
            (
                lambda client, path, data=None, format=None: client.patch(
                    path, data, format
                )
            ),
            # delete
            (lambda client, path, data=None, format=None: client.delete(path)),
        ],
    )
    def test_pk_permission_denied(self, action):
        """We can only view/update/delete self user by using `pk=<not-a-number>`"""
        authenticate(self.client, self.data["username"], self.data["password"])
        response = action(
            self.client,
            # using a number for the pk would mean we're trying to access CRUD
            # operations on a specific user which is forbidden
            reverse_lazy("user-detail", kwargs={"pk": 1}),
            self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )

    def test_update_user(self):
        authenticate(self.client, self.data["username"], self.data["password"])
        data = {**self.data, "first_name": "Firstname1", "last_name": "Lastname 1"}
        response = self.client.put(
            reverse_lazy("user-detail", kwargs={"pk": None}), data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        data.pop("password")
        assert response.data == {
            **data,
            "id": 1,
        }

    def test_partial_update_user(self):
        """Using a patch for a partial update (not all fields)."""
        authenticate(self.client, self.data["username"], self.data["password"])
        data = {"first_name": "Firstname1", "last_name": "Lastname 1"}
        response = self.client.patch(
            reverse_lazy("user-detail", kwargs={"pk": None}), data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "username": self.data["username"],
            "email": "",
            **data,
        }

    def test_delete_user(self):
        authenticate(self.client, self.data["username"], self.data["password"])
        response = self.client.delete(reverse_lazy("user-detail", kwargs={"pk": None}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert User.objects.count() == 0


@pytest.mark.django_db
class TestAccountRegister:
    client = APIClient()
    url = reverse_lazy("register")
    username = {"username": "username1"}
    password = {"password": "password1"}
    data = {**username, **password}

    def test_url(self):
        assert self.url == "/account/register"

    @freeze_time("2021-01-16 16:00:00")
    def test_create(self):
        assert User.objects.filter(**self.username).count() == 0
        response = self.client.post(self.url, self.data, format="json")
        assert response.data == {
            "id": 1,
            "username": "username1",
            "first_name": "",
            "last_name": "",
            "email": "",
        }
        assert response.status_code == status.HTTP_201_CREATED
        users = User.objects.filter(**self.username)
        assert users.count() == 1
        user = users.get()
        assert user.check_password(self.password["password"]) is True
        assert user.nurse is not None

    def test_create_already_exists(self):
        assert User.objects.filter(**self.username).count() == 0
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(**self.username).count() == 1
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["username"][0] == "A user with that username already exists."
        )
        assert User.objects.filter(**self.username).count() == 1

    def test_get(self):
        """It's not allowed to list all users."""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data == {"detail": 'Method "GET" not allowed.'}

    def test_auth_ok(self):
        """Note this isn't a REST endpoint."""
        url = reverse_lazy("rest_framework:login")
        assert url == "/account/login/"
        user = User.objects.create(**self.username)
        user.set_password(self.password["password"])
        user.save()
        response = self.client.post(url, self.data)
        assert response.status_code == status.HTTP_302_FOUND
        # redirecting to the profile page
        assert response.get("Location") == "/accounts/profile/"

    def test_auth_error(self):
        url = reverse_lazy("rest_framework:login")
        response = self.client.post(url, self.data)
        assert response.status_code == status.HTTP_200_OK
        assert (
            "Please enter a correct username and password" in response.content.decode()
        )


@pytest.mark.django_db
class TestProfile:

    client = APIClient()

    url = "/profile/"

    username = "username1"
    password = "password1"

    def test_endpoint(self):
        assert self.url == reverse_lazy("profile")

    def test_get(self):
        authenticate(self.client, self.username, self.password)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": 1,
            "username": "username1",
            "first_name": "",
            "last_name": "",
            "email": "",
        }
