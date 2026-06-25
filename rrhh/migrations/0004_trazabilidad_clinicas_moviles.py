from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rrhh", "0003_clinicas_moviles"),
    ]

    operations = [
        migrations.AddField(
            model_name="agendaclinicamovil",
            name="actualizado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clinicas_moviles_actualizadas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="agendaclinicamovil",
            name="creado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clinicas_moviles_creadas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
