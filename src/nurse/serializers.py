from rest_framework import serializers

from .models import Patient, Prescription, make_phone_field


class PatientSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=30, allow_blank=False)
    lastname = serializers.CharField(max_length=30, allow_blank=False)
    address = serializers.CharField(max_length=300, allow_blank=False)
    zip_code = serializers.CharField(allow_blank=False, max_length=5)
    city = serializers.CharField(max_length=300, allow_blank=False)
    phone = make_phone_field()

    def create(self, validated_data):
        return Patient.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.address = validated_data.get("address", instance.address)
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        instance.city = validated_data.get("city", instance.city)
        instance.phone = validated_data.get("phone", instance.phone)
        return instance


class PrescriptionSerializer(serializers.Serializer):
    carte_vitale = serializers.CharField(max_length=300, allow_blank=False)
    caisse_rattachement = serializers.CharField(max_length=300, allow_blank=False)
    prescribing_doctor = serializers.CharField(max_length=300, allow_blank=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    at_renew = serializers.BooleanField()
    photo_prescription = serializers.CharField(max_length=300, allow_blank=True)
    patient = serializers.CharField(max_length=300, allow_blank=False)

    def create(self, validated_data):
        return Prescription.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.carte_vitale = validated_data.get(
            "carte_vitale", instance.carte_vitale
        )
        instance.caisse_rattachement = validated_data.get(
            "caisse_rattachement", instance.caisse_rattachement
        )
        instance.prescribing_doctor = validated_data.get(
            "prescribing_doctor", instance.prescribing_doctor
        )
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.at_renew = validated_data.get("at_renew", instance.at_renew)
        instance.photo_prescription = validated_data.get(
            "photo_prescription", instance.photo_prescription
        )
        instance.patient = validated_data.get("patient", instance.patient)
        return instance
