from django.contrib.auth.models import User
from nurse.models import Nurse, Patient, Prescription
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    prescriptions = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"

    def get_prescriptions(self, obj):
        prescriptions = Prescription.objects.filter(patient_id=obj.id).order_by(
            "-end_date"
        )[:2]
        return PrescriptionSerializer(prescriptions, many=True).data


class PrescriptionSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = "__all__"

    def get_is_valid(self, obj):
        return obj.is_valid()


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
