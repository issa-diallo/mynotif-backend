from nurse.views import PatientViewSet, PrescriptionViewSet, NurseViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("patient", PatientViewSet)
router.register("prescription", PrescriptionViewSet)
router.register("nurse", NurseViewSet)
router.register("user", UserViewSet)
