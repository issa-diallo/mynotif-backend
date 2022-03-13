from django.urls import path
from rest_framework import routers
from nurse.views import (
    PatientViewSet,
    PrescriptionViewSet,
    NurseViewSet,
    UserViewSet,
    ProfileView,
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
