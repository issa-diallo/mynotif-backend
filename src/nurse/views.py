from django.contrib.auth.models import User
from nurse.models import Nurse, Patient, Prescription
from nurse.serializers import (
    NurseSerializer,
    PatientSerializer,
    PrescriptionSerializer,
    UserSerializer,
)
from rest_framework import viewsets


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
