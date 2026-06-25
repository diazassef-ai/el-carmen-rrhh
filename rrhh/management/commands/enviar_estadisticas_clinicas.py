from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from rrhh.clinicas_reportes import correos_reportes_clinicas, enviar_estadisticas_clinicas, nombre_periodo


class Command(BaseCommand):
    help = "Envia por correo el resumen mensual de clinicas moviles."

    def add_arguments(self, parser):
        parser.add_argument("--anio", type=int, help="Ano del reporte. Por defecto usa el mes anterior.")
        parser.add_argument("--mes", type=int, help="Mes del reporte. Por defecto usa el mes anterior.")

    def handle(self, *args, **options):
        anio = options.get("anio")
        mes = options.get("mes")
        if not anio or not mes:
            primer_dia_mes = timezone.localdate().replace(day=1)
            mes_anterior = primer_dia_mes - timedelta(days=1)
            anio = mes_anterior.year
            mes = mes_anterior.month
        try:
            date(anio, mes, 1)
        except ValueError as exc:
            raise CommandError("Debe indicar un ano y mes validos.") from exc

        destinatarios = correos_reportes_clinicas()
        if not destinatarios:
            raise CommandError("No hay destinatarios. Configure emails de usuarios o DJANGO_CLINICAS_REPORT_EMAILS.")

        enviados = enviar_estadisticas_clinicas(anio, mes, destinatarios)
        self.stdout.write(self.style.SUCCESS(
            f"Resumen {nombre_periodo(anio, mes)} enviado a {enviados} destinatario(s)."
        ))
