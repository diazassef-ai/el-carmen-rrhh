from django.db import migrations


PERFILES = [
    "Administrador",
    "Secretaria",
    "Jefes de programa",
    "Solo Lectura",
    "Visualizacion calendario",
]


def crear_perfiles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for nombre in PERFILES:
        Group.objects.get_or_create(name=nombre)


def eliminar_perfiles(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("rrhh", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(crear_perfiles, eliminar_perfiles),
    ]
