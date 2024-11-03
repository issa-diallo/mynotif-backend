from datetime import datetime, timedelta

import pytest

from nurse.models import Patient, Prescription


@pytest.fixture
def patient():
    patient_data = {
        "firstname": "John",
        "lastname": "Leen",
        "street": "3 place du cerdan",
        "zip_code": "95400",
        "city": "courdimanche",
        "phone": "0602015454",
        "health_card_number": "12345678910",
        "ss_provider_code": "123456789",
        "birthday": "2023-08-15",
    }
    patient = Patient.objects.create(**patient_data)
    yield patient


# Fixture for prescriptions that will be common across all tests.
@pytest.fixture
def base_prescriptions(patient):
    Prescription.objects.create(
        patient=patient,
        prescribing_doctor="Dr A",
        email_doctor="dr.a@example.com",
        start_date=datetime.now().date() - timedelta(days=3),
        end_date=datetime.now().date() + timedelta(days=3),
    )
    Prescription.objects.create(
        patient=patient,
        prescribing_doctor="Dr B",
        email_doctor="dr.b@example.com",
        start_date=datetime.now().date() - timedelta(days=10),
        end_date=datetime.now().date() + timedelta(days=9),
    )


# Separate fixtures for different prescription types.
@pytest.fixture
def prescription_expiring_today(patient):
    Prescription.objects.create(
        patient=patient,
        prescribing_doctor="Dr C",
        email_doctor="dr.c@example.com",
        start_date=datetime.now().date() - timedelta(days=5),
        end_date=datetime.now().date(),
    )


@pytest.fixture
def prescription_started_today(patient):
    Prescription.objects.create(
        patient=patient,
        prescribing_doctor="Dr D",
        email_doctor="dr.d@example.com",
        start_date=datetime.now().date(),
        end_date=datetime.now().date() + timedelta(days=5),
    )


@pytest.mark.django_db
class TestPrescription:
    def test_str(self, base_prescriptions):
        prescription = Prescription.objects.first()
        assert prescription.__str__() == "Prescription: Dr A"


@pytest.mark.django_db
class TestPrescriptionManager:
    @pytest.mark.parametrize(
        "days,expected_count,expected_doctors",
        [
            (7, 1, ["Dr A"]),
            (11, 2, ["Dr A", "Dr B"]),
        ],
    )
    def test_prescriptions_expiring_soon(
        self, base_prescriptions, days, expected_count, expected_doctors
    ):
        prescriptions = Prescription.objects.expiring_soon(days=days)
        assert prescriptions.count() == expected_count
        retrieved_doctors = [
            prescription.prescribing_doctor for prescription in prescriptions
        ]
        assert sorted(retrieved_doctors) == expected_doctors

    def test_prescription_expiring_today(self, prescription_expiring_today):
        prescriptions = Prescription.objects.expiring_soon(days=0)
        assert prescriptions.count() == 1
        assert prescriptions.first().prescribing_doctor == "Dr C"

    def test_prescription_started_today(self, prescription_started_today):
        prescriptions = Prescription.objects.expiring_soon(days=5)
        assert prescriptions.count() == 1
        assert prescriptions.first().prescribing_doctor == "Dr D"

    def test_no_prescriptions(self):
        prescriptions = Prescription.objects.expiring_soon()
        assert prescriptions.count() == 0

    def test_prescriptions_email_doctor(self, base_prescriptions):
        prescription = Prescription.objects.first()
        assert prescription.email_doctor == "dr.a@example.com"
