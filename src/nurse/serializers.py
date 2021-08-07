from django.contrib.auth.models import User
from nurse.models import Nurse, Patient, Prescription
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
