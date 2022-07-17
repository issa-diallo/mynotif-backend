from django.urls import path
from rest_framework import routers

from nurse.views import (
    NurseViewSet,
    PatientViewSet,
    PrescriptionViewSet,
    ProfileView,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register("patient", PatientViewSet)
router.register("prescription", PrescriptionViewSet)
router.register("nurse", NurseViewSet)
router.register("user", UserViewSet)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
]

urlpatterns += router.urls
