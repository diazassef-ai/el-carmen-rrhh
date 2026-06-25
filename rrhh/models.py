from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


def validar_adjunto_rrhh(archivo):
    extension = archivo.name.rsplit(".", 1)[-1].lower()
    if extension not in {"pdf", "jpg", "jpeg", "png"}:
        raise ValidationError("Solo se permiten archivos PDF, JPG o PNG.")


class Funcionario(models.Model):
    TIPOS_CONTRATO = [
        ("Planta", "Planta"),
        ("Contrata", "Contrata"),
        ("Honorarios", "Honorarios"),
        ("Reemplazo", "Reemplazo"),
        ("Otro", "Otro"),
    ]

    rut = models.CharField(max_length=12, unique=True)
    nombre_completo = models.CharField(max_length=180)
    cargo = models.CharField(max_length=140)
    tipo_contrato = models.CharField(max_length=30, choices=TIPOS_CONTRATO)
    unidad = models.CharField(max_length=120)
    correo_electronico = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre_completo"]
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"

    def __str__(self):
        return f"{self.nombre_completo} ({self.rut})"

    def get_absolute_url(self):
        return reverse("rrhh_funcionario_ficha", args=[self.pk])

    @property
    def total_permisos(self):
        return self.solicitudes.exclude(tipo_solicitud="Capacitacion").count()

    @property
    def total_capacitaciones(self):
        return self.solicitudes.filter(tipo_solicitud="Capacitacion").count()

    @property
    def total_dias_ausentes(self):
        return sum(s.numero_dias or 0 for s in self.solicitudes.aprobadas())


class SolicitudQuerySet(models.QuerySet):
    def aprobadas(self):
        return self.filter(estado="Aprobado")

    def vigentes_en(self, fecha):
        return self.filter(
            fecha_desde__lte=fecha,
            fecha_hasta__gte=fecha,
        ).exclude(estado__in=["Rechazado", "Anulado"])


class PermisoCapacitacion(models.Model):
    TIPOS_SOLICITUD = [
        ("Feriado legal", "Feriado legal"),
        ("Permiso con goce de remuneraciones", "Permiso con goce de remuneraciones"),
        ("Permiso sin goce de remuneraciones", "Permiso sin goce de remuneraciones"),
        ("Devolucion de tiempo libre", "Devolucion de tiempo libre"),
        ("Licencia medica", "Licencia medica"),
        ("Comision de servicio", "Comision de servicio"),
        ("Capacitacion", "Capacitacion"),
        ("Otro permiso", "Otro permiso"),
    ]
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado"),
        ("Anulado", "Anulado"),
    ]
    MODALIDADES = [
        ("Presencial", "Presencial"),
        ("Online", "Online"),
        ("Mixta", "Mixta"),
    ]

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="solicitudes",
    )
    tipo_solicitud = models.CharField(max_length=60, choices=TIPOS_SOLICITUD)
    numero_dias = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    hora_desde = models.TimeField(null=True, blank=True)
    hora_hasta = models.TimeField(null=True, blank=True)
    dias_pendientes = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    observaciones = models.TextField(blank=True)
    fecha_entrega_solicitante = models.DateField(null=True, blank=True)
    fecha_recepcion_oficina_personal = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")
    nombre_capacitacion = models.CharField(max_length=180, blank=True)
    institucion_organizadora = models.CharField(max_length=180, blank=True)
    modalidad = models.CharField(max_length=20, choices=MODALIDADES, blank=True)
    lugar = models.CharField(max_length=180, blank=True)
    observaciones_capacitacion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    objects = SolicitudQuerySet.as_manager()

    class Meta:
        ordering = ["-fecha_desde", "funcionario__nombre_completo"]
        verbose_name = "Permiso o capacitacion"
        verbose_name_plural = "Permisos y capacitaciones"

    def __str__(self):
        return f"{self.funcionario} - {self.tipo_solicitud} ({self.fecha_desde})"

    def get_absolute_url(self):
        return reverse("rrhh_solicitud_detalle", args=[self.pk])

    def clean(self):
        if self.fecha_desde and self.fecha_hasta and self.fecha_hasta < self.fecha_desde:
            raise ValidationError("La fecha de termino no puede ser anterior a la fecha de inicio.")
        if self.hora_desde and self.hora_hasta and self.hora_hasta <= self.hora_desde:
            raise ValidationError("La hora de termino debe ser posterior a la hora de inicio.")
        if self.tipo_solicitud == "Capacitacion" and not self.nombre_capacitacion:
            raise ValidationError("Las capacitaciones deben incluir el nombre de la capacitacion.")

    def save(self, *args, **kwargs):
        if self.fecha_desde and self.fecha_hasta and not self.numero_dias:
            self.numero_dias = (self.fecha_hasta - self.fecha_desde).days + 1
        super().save(*args, **kwargs)

    @property
    def es_capacitacion(self):
        return self.tipo_solicitud == "Capacitacion"

    @property
    def fecha_retorno(self):
        return self.fecha_hasta + timedelta(days=1)

    @property
    def horario(self):
        if self.hora_desde and self.hora_hasta:
            return f"{self.hora_desde:%H:%M} - {self.hora_hasta:%H:%M}"
        return "Dia completo"

    @property
    def color_calendario(self):
        colores = {
            "Feriado legal": "#2563eb",
            "Capacitacion": "#16a34a",
            "Licencia medica": "#dc2626",
            "Comision de servicio": "#eab308",
            "Permiso con goce de remuneraciones": "#7c3aed",
            "Permiso sin goce de remuneraciones": "#7c3aed",
            "Devolucion de tiempo libre": "#7c3aed",
            "Otro permiso": "#64748b",
        }
        return colores.get(self.tipo_solicitud, "#64748b")

    def rango_fechas(self):
        fecha = self.fecha_desde
        while fecha <= self.fecha_hasta:
            yield fecha
            fecha += timedelta(days=1)


class DocumentoAdjunto(models.Model):
    solicitud = models.ForeignKey(
        PermisoCapacitacion,
        on_delete=models.CASCADE,
        related_name="adjuntos",
    )
    archivo = models.FileField(
        upload_to="permisos/",
        validators=[validar_adjunto_rrhh],
    )
    nombre = models.CharField(max_length=180, blank=True)
    subido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subido_en"]
        verbose_name = "Documento adjunto"
        verbose_name_plural = "Documentos adjuntos"

    def __str__(self):
        return self.nombre or self.archivo.name

    def save(self, *args, **kwargs):
        if not self.nombre and self.archivo:
            self.nombre = self.archivo.name.rsplit("/", 1)[-1]
        super().save(*args, **kwargs)


class ClinicaMovil(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.CharField(max_length=240, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Clinica movil"
        verbose_name_plural = "Clinicas moviles"

    def __str__(self):
        return self.nombre


class AgendaClinicaMovil(models.Model):
    ESTADOS = [
        ("Programada", "Programada"),
        ("Confirmada", "Confirmada"),
        ("Suspendida", "Suspendida"),
        ("Realizada", "Realizada"),
    ]

    clinica = models.ForeignKey(
        ClinicaMovil,
        on_delete=models.PROTECT,
        related_name="agendamientos",
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField(null=True, blank=True)
    lugar = models.CharField(max_length=220)
    sector = models.CharField(max_length=160, blank=True)
    cupos_totales = models.PositiveIntegerField(default=0)
    cupos_reservados = models.PositiveIntegerField(default=0)
    responsable = models.CharField(max_length=160, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Programada")
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha", "hora_inicio", "clinica__nombre"]
        verbose_name = "Agendamiento de clinica movil"
        verbose_name_plural = "Agendamientos de clinicas moviles"

    def __str__(self):
        return f"{self.clinica} - {self.fecha} {self.hora_inicio:%H:%M}"

    def clean(self):
        if self.hora_inicio and self.hora_termino and self.hora_termino <= self.hora_inicio:
            raise ValidationError("La hora de termino debe ser posterior a la hora de inicio.")
        if self.cupos_reservados > self.cupos_totales:
            raise ValidationError("Los cupos reservados no pueden superar los cupos totales.")

    @property
    def cupos_disponibles(self):
        return max(self.cupos_totales - self.cupos_reservados, 0)

    @property
    def horario(self):
        if self.hora_termino:
            return f"{self.hora_inicio:%H:%M} - {self.hora_termino:%H:%M}"
        return f"{self.hora_inicio:%H:%M}"

    @property
    def color_calendario(self):
        if self.estado == "Suspendida":
            return "#dc2626"
        if self.clinica.nombre.endswith("1"):
            return "#0f766e"
        return "#2563eb"


def solicitudes_del_mes(fecha=None):
    fecha = fecha or timezone.localdate()
    return PermisoCapacitacion.objects.filter(
        fecha_desde__year=fecha.year,
        fecha_desde__month=fecha.month,
    )
