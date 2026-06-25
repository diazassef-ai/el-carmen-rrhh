from django.db import migrations, models
import django.db.models.deletion


def crear_datos_iniciales(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    ClinicaMovil = apps.get_model("rrhh", "ClinicaMovil")

    Group.objects.get_or_create(name="Agendamiento clinicas moviles")
    ClinicaMovil.objects.get_or_create(
        nombre="Clinica movil 1",
        defaults={"descripcion": "Primera clinica movil institucional"},
    )
    ClinicaMovil.objects.get_or_create(
        nombre="Clinica movil 2",
        defaults={"descripcion": "Segunda clinica movil institucional"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ("rrhh", "0002_perfiles_rrhh"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClinicaMovil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120, unique=True)),
                ("descripcion", models.CharField(blank=True, max_length=240)),
                ("activa", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Clinica movil",
                "verbose_name_plural": "Clinicas moviles",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="AgendaClinicaMovil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("hora_inicio", models.TimeField()),
                ("hora_termino", models.TimeField(blank=True, null=True)),
                ("lugar", models.CharField(max_length=220)),
                ("sector", models.CharField(blank=True, max_length=160)),
                ("cupos_totales", models.PositiveIntegerField(default=0)),
                ("cupos_reservados", models.PositiveIntegerField(default=0)),
                ("responsable", models.CharField(blank=True, max_length=160)),
                ("estado", models.CharField(choices=[("Programada", "Programada"), ("Confirmada", "Confirmada"), ("Suspendida", "Suspendida"), ("Realizada", "Realizada")], default="Programada", max_length=20)),
                ("observaciones", models.TextField(blank=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("clinica", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="agendamientos", to="rrhh.clinicamovil")),
            ],
            options={
                "verbose_name": "Agendamiento de clinica movil",
                "verbose_name_plural": "Agendamientos de clinicas moviles",
                "ordering": ["fecha", "hora_inicio", "clinica__nombre"],
            },
        ),
        migrations.RunPython(crear_datos_iniciales, migrations.RunPython.noop),
    ]
