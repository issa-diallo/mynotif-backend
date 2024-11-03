from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from nurse.management.commands._notifications import notify
from nurse.models import Nurse, Patient, Prescription, UserOneSignalProfile
from nurse.serializers import (
    ExpandedPrescriptionSerializer,
    NurseSerializer,
    PatientSerializer,
    PrescriptionEmailSerializer,
    PrescriptionFileSerializer,
    UserOneSignalProfileSerializer,
    UserSerializer,
    UserSerializerV2,
)
from nurse.utils.email import send_mail_with_reply


class DynamicFieldsMixin:
    """
    A mixin that allows specifying a subset of fields to be returned by the serializer.

    This mixin checks for a 'fields' parameter in the query. If 'fields' is present,
    it should be a comma-separated list of field names (e.g., 'id,firstname,lastname').
    This list is then passed to the serializer to limit the serialized fields to only
    those specified.

    Example:
        GET /api/resource/?fields=id,name,description
        This would return only the specified fields for each resource.

    Methods:
        get_serializer(*args, **kwargs): Returns a serializer instance with dynamically
                                         filtered fields.
    """

    def get_serializer(self, *args, **kwargs):
        # Retrieve `fields` from query parameters
        fields = self.request.query_params.get("fields")
        if fields:
            # Convert comma-separated string to list
            fields = fields.split(",")
            kwargs["fields"] = fields
        return super().get_serializer(*args, **kwargs)


class SendEmailToDoctorView(APIView):
    def post(self, request, pk):
        serializer = PrescriptionEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prescription = get_object_or_404(Prescription, id=pk)
        patient = prescription.patient
        email_doctor = prescription.email_doctor
        if not email_doctor:
            return Response(
                {"error": "Doctor has no email"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        nurse, _ = Nurse.objects.get_or_create(user=user)

        if not nurse.patients.filter(id=patient.id).exists():
            return Response(
                {"error": "You are not authorized to send emails to this patient"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not user.first_name or not user.last_name or not user.email:
            return Response(
                {
                    "error": (
                        "Please update your profile with your first and last name "
                        "and email"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        subject = "Renouveler ordonnance"

        html_message = render_to_string(
            "emails/email_template.html",
            {
                "patient_name": f"{patient.firstname} {patient.lastname}",
                "patient_birth_date": patient.birthday,
                "nurse_name": f"{user.first_name} {user.last_name}",
                "additional_info": serializer.validated_data["additional_info"],
            },
        )
        try:
            send_mail_with_reply(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [email_doctor],
                reply_to_email=user.email,
                fail_silently=False,
                html_message=html_message,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"message": "Email sent"}, status=status.HTTP_200_OK)


class PatientViewSet(DynamicFieldsMixin, viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        """Only the patients associated to the logged in nurse."""
        queryset = self.queryset
        nurse, _ = Nurse.objects.get_or_create(user=self.request.user)
        queryset = queryset.filter(nurse=nurse)
        return queryset

    def create(self, request):
        nurse, _ = Nurse.objects.get_or_create(user=self.request.user)
        response = super().create(request)
        patient = Patient.objects.get(id=response.data["id"])
        patient.nurse_set.add(nurse)
        return response


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = ExpandedPrescriptionSerializer

    def get_queryset(self):
        """Only the prescriptions associated to the logged in nurse."""
        queryset = self.queryset
        nurse, _ = Nurse.objects.get_or_create(user=self.request.user)
        queryset = queryset.filter(patient__nurse=nurse)
        return queryset


class PrescriptionFileView(generics.UpdateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionFileSerializer


class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer


class UserOneSignalProfileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserOneSignalProfile.objects.all()
    serializer_class = UserOneSignalProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        profile = queryset.first()
        if profile:
            serializer = self.get_serializer(profile)
            return Response([serializer.data])
        return Response([])

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), user=request.user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class ProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Retrieve, update, destroy and list, but no create.
    For Create, see `UserCreate` below.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Fecthing a specific object other than `request.user` isn't allowed."""
        if self.kwargs.get("pk").isdigit():
            raise PermissionDenied()
        return self.request.user


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def _create_nurse(self, response_data):
        """
        Protected method to create or get the associated Nurse instance.
        """
        username = response_data["username"]
        user = User.objects.get(username=username)
        Nurse.objects.get_or_create(user=user)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self._create_nurse(response.data)
        return response


class UserCreateV2(UserCreate):
    """Create a User using email and password."""

    serializer_class = UserSerializerV2

    def _create_nurse(self, response_data):
        """
        Override `_create_nurse` to use email as the username.
        """
        email = response_data["email"]
        user = User.objects.get(username=email)
        Nurse.objects.get_or_create(user=user)


class AdminNotificationView(APIView):
    """The view dealing with sending push notifications."""

    permission_classes = [IsAdminUser]

    def post(self, request):
        notify()
        return Response(status=status.HTTP_204_NO_CONTENT)
