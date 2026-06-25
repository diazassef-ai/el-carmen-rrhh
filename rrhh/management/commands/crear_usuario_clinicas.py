import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea o actualiza el usuario operativo de agendamiento de clinicas moviles."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_CLINICAS_USERNAME", "clinicas").strip()
        email = os.environ.get("DJANGO_CLINICAS_EMAIL", "").strip()
        password = os.environ.get("DJANGO_CLINICAS_PASSWORD", "").strip()

        if not username or not password:
            self.stdout.write(
                "Usuario de clinicas omitido: define DJANGO_CLINICAS_PASSWORD para crearlo."
            )
            return

        group, _ = Group.objects.get_or_create(name="Agendamiento clinicas moviles")
        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save()
        user.groups.set([group])

        action = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Usuario de clinicas {action}: {username}"))
