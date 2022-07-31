"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as drf_yasg_get_schema_view
from rest_framework import permissions, routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

from nurse import views as nurse_views
from nurse.urls import router as nurse_router

router = routers.DefaultRouter()
router.registry.extend(nurse_router.registry)

title = "Mynotif"
description = "API Mynotif"
version = "1.0.0"

schema_view = drf_yasg_get_schema_view(
    openapi.Info(
        title=title,
        default_version=version,
        description=description,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("rest_framework.urls")),
    path("account/register", nurse_views.UserCreate.as_view(), name="register"),
    path("", include("nurse.urls"), name="nurse"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("", include(router.urls)),
    path(
        "openapi",
        get_schema_view(
            title=title,
            description=description,
            version=version,
            permission_classes=[AllowAny],
        ),
        name="openapi-schema",
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
