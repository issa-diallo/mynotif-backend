import os

from django.http import JsonResponse


def version(request):
    version = os.environ.get("VERSION") or "0.0.0"
    return JsonResponse({"version": version})
