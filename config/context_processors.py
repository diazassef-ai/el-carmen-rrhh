from django.conf import settings


def security_settings(request):
    return {
        "IDLE_TIMEOUT_SECONDS": settings.IDLE_TIMEOUT_SECONDS,
    }
