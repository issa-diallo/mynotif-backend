from django.urls import path
from rest_framework import routers

from nurse.views import (
    AdminNotificationView,
    NurseViewSet,
    PatientViewSet,
    PrescriptionFileView,
    PrescriptionViewSet,
    ProfileView,
    SendEmailToDoctorView,
    StripeProductViewSet,
    SubscriptionCancelView,
    SubscriptionSuccessView,
    SubscriptionViewSet,
    UserOneSignalProfileViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register("patient", PatientViewSet)
router.register("prescription", PrescriptionViewSet)
router.register("nurse", NurseViewSet)
router.register("user", UserViewSet)
router.register("onesignal", UserOneSignalProfileViewSet)
router.register("subscription", SubscriptionViewSet)
router.register("stripe-products", StripeProductViewSet)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "prescription/upload/<int:pk>/",
        PrescriptionFileView.as_view(),
        name="prescription-upload",
    ),
    path("notify/", AdminNotificationView.as_view(), name="notify"),
    path(
        "prescription/<int:pk>/send-email/",
        SendEmailToDoctorView.as_view(),
        name="send-email-to-doctor",
    ),
    path(
        "subscriptions/success/",
        SubscriptionSuccessView.as_view(),
        name="subscription-success",
    ),
    path(
        "subscriptions/cancel/",
        SubscriptionCancelView.as_view(),
        name="subscription-cancel",
    ),
]

urlpatterns += router.urls
