import os
from calendar import monthrange
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Count, Sum

from .models import AgendaClinicaMovil


MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def periodo_mensual(anio, mes):
    inicio = date(anio, mes, 1)
    fin = date(anio, mes, monthrange(anio, mes)[1])
    return inicio, fin


def nombre_periodo(anio, mes):
    return f"{MESES[mes - 1].capitalize()} {anio}"


def agendamientos_del_mes(anio, mes):
    inicio, fin = periodo_mensual(anio, mes)
    return AgendaClinicaMovil.objects.select_related(
        "clinica",
        "creado_por",
        "actualizado_por",
    ).filter(fecha__gte=inicio, fecha__lte=fin)


def construir_estadisticas_clinicas(anio, mes):
    agendas = agendamientos_del_mes(anio, mes)
    totales = agendas.aggregate(
        total=Count("id"),
        cupos_totales=Sum("cupos_totales"),
        cupos_reservados=Sum("cupos_reservados"),
    )
    cupos_totales = totales["cupos_totales"] or 0
    cupos_reservados = totales["cupos_reservados"] or 0
    cupos_disponibles = max(cupos_totales - cupos_reservados, 0)
    ocupacion = round((cupos_reservados / cupos_totales) * 100, 1) if cupos_totales else 0

    por_clinica = []
    for fila in agendas.values("clinica__nombre").annotate(
        total=Count("id"),
        cupos_totales=Sum("cupos_totales"),
        cupos_reservados=Sum("cupos_reservados"),
    ).order_by("clinica__nombre"):
        fila["cupos_totales"] = fila["cupos_totales"] or 0
        fila["cupos_reservados"] = fila["cupos_reservados"] or 0
        fila["cupos_disponibles"] = max(fila["cupos_totales"] - fila["cupos_reservados"], 0)
        fila["ocupacion"] = round((fila["cupos_reservados"] / fila["cupos_totales"]) * 100, 1) if fila["cupos_totales"] else 0
        por_clinica.append(fila)

    por_lugar = agendas.values("lugar", "sector").annotate(
        total=Count("id"),
        cupos_totales=Sum("cupos_totales"),
        cupos_reservados=Sum("cupos_reservados"),
    ).order_by("lugar", "sector")

    usuarios = {}
    for agenda in agendas:
        usuario = agenda.creado_por or agenda.actualizado_por
        if usuario:
            usuarios[usuario.pk] = usuario

    return {
        "agendas": agendas.order_by("fecha", "hora_inicio"),
        "periodo": nombre_periodo(anio, mes),
        "anio": anio,
        "mes": mes,
        "totales": {
            "total": totales["total"] or 0,
            "cupos_totales": cupos_totales,
            "cupos_reservados": cupos_reservados,
            "cupos_disponibles": cupos_disponibles,
            "ocupacion": ocupacion,
        },
        "por_clinica": por_clinica,
        "por_lugar": por_lugar,
        "usuarios_agendamiento": sorted(usuarios.values(), key=lambda user: user.get_full_name() or user.username),
    }


def correos_reportes_clinicas():
    correos = set()
    try:
        grupo = Group.objects.get(name="Agendamiento clinicas moviles")
    except Group.DoesNotExist:
        grupo = None
    if grupo:
        correos.update(
            user.email.strip()
            for user in grupo.user_set.filter(is_active=True).exclude(email="")
            if user.email and user.email.strip()
        )
    correos.update(
        correo.strip()
        for correo in os.environ.get("DJANGO_CLINICAS_REPORT_EMAILS", "").split(",")
        if correo.strip()
    )
    return sorted(correos)


def construir_cuerpo_correo_clinicas(anio, mes):
    datos = construir_estadisticas_clinicas(anio, mes)
    lineas = [
        f"Resumen de clinicas moviles - {datos['periodo']}",
        "",
        f"Agendamientos: {datos['totales']['total']}",
        f"Cupos totales: {datos['totales']['cupos_totales']}",
        f"Cupos reservados: {datos['totales']['cupos_reservados']}",
        f"Cupos disponibles: {datos['totales']['cupos_disponibles']}",
        f"Ocupacion: {datos['totales']['ocupacion']}%",
        "",
        "Detalle por clinica:",
    ]
    for item in datos["por_clinica"]:
        lineas.append(
            f"- {item['clinica__nombre']}: {item['total']} agendamientos, "
            f"{item['cupos_reservados']}/{item['cupos_totales']} cupos, "
            f"{item['cupos_disponibles']} disponibles"
        )
    if not datos["por_clinica"]:
        lineas.append("- Sin agendamientos en el periodo.")
    return "\n".join(lineas)


def enviar_estadisticas_clinicas(anio, mes, destinatarios=None):
    destinatarios = destinatarios or correos_reportes_clinicas()
    if not destinatarios:
        return 0
    asunto = f"Estadisticas clinicas moviles - {nombre_periodo(anio, mes)}"
    cuerpo = construir_cuerpo_correo_clinicas(anio, mes)
    enviados = send_mail(
        asunto,
        cuerpo,
        settings.DEFAULT_FROM_EMAIL,
        destinatarios,
        fail_silently=False,
    )
    return len(destinatarios) if enviados else 0
