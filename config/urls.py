from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import include, path


def cerrar_sesion(request):
    logout(request)
    return render(request, "registration/logged_out.html")


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", cerrar_sesion, name="logout"),
    path("", include("rrhh.urls")),
    path("rrhh/", include("rrhh.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
