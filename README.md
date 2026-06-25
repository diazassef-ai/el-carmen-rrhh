# EL CARMEN RRHH

Aplicacion Django independiente para gestionar permisos, capacitaciones y ausentismo del personal del CESFAM El Carmen.

## Instalacion local

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Rutas

- Sistema: `http://127.0.0.1:8000/`
- Calendario visual: `http://127.0.0.1:8000/calendario/visualizacion/`
- Admin Django: `http://127.0.0.1:8000/django-admin/`

## Validacion

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --dry-run --noinput
```

## Despliegue en Render

El proyecto incluye `render.yaml` para desplegarlo como Blueprint en Render.

Pasos:

1. Subir esta carpeta a un repositorio GitHub.
2. En Render, crear un `New Blueprint Instance`.
3. Conectar el repositorio.
4. Aplicar el blueprint.
5. En las variables de entorno del servicio, completar `DJANGO_SUPERUSER_PASSWORD`.
6. Hacer redeploy. El comando `crear_admin_inicial` creara o actualizara el usuario administrador.

El blueprint crea:

- Web service `el-carmen-rrhh`
- Variables de entorno de produccion

Nota: este blueprint no crea PostgreSQL para evitar cobros en Render. Usa SQLite para pruebas. Para uso institucional real se recomienda agregar PostgreSQL o un servicio de base de datos persistente.

## Variables de produccion

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=0`
- `DJANGO_PRODUCTION=1`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `DJANGO_SESSION_COOKIE_AGE`: segundos de duracion de sesion por inactividad. Valor por defecto: `1800`.
- `DJANGO_IDLE_TIMEOUT_SECONDS`: segundos para cierre automatico en navegador. Valor por defecto: igual a `DJANGO_SESSION_COOKIE_AGE`.
- `DJANGO_SUPERUSER_USERNAME`: usuario administrador inicial. Valor sugerido: `admin`.
- `DJANGO_SUPERUSER_EMAIL`: correo del administrador inicial.
- `DJANGO_SUPERUSER_PASSWORD`: clave del administrador inicial. Obligatoria en Render Free porque no hay Shell.
- `DJANGO_CLINICAS_USERNAME`: usuario operativo para clinicas moviles. Valor sugerido: `clinicas`.
- `DJANGO_CLINICAS_EMAIL`: correo del usuario operativo de clinicas moviles.
- `DJANGO_CLINICAS_PASSWORD`: clave del usuario operativo de clinicas moviles.
- `DJANGO_CLINICAS_REPORT_EMAILS`: correos extra para recibir estadisticas de clinicas, separados por coma.
- `EMAIL_BACKEND`: backend de correo. En local usa consola por defecto.
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`: configuracion SMTP para envio real.

## Seguridad de sesion

La plataforma cierra la sesion por inactividad a nivel servidor y navegador. Al usar "Cerrar sesion" en una ventana, las demas pestanas abiertas detectan el cierre y vuelven al login.

## Clinicas moviles

El sistema incluye un modulo para agendar dos clinicas moviles, registrar lugar, sector, horario, cupos totales y cupos reservados. El calendario muestra los cupos disponibles por agendamiento.

La seccion `Clinicas Moviles > Estadisticas Clinicas` permite revisar estadisticas por mes, ver cupos por clinica y lugar, y enviar el resumen mensual a los correos vinculados. El envio considera usuarios activos del grupo `Agendamiento clinicas moviles` que tengan email y los correos definidos en `DJANGO_CLINICAS_REPORT_EMAILS`.

Para automatizar el envio mensual, programe el comando:

```powershell
python manage.py enviar_estadisticas_clinicas
```

Tambien se puede enviar un periodo especifico:

```powershell
python manage.py enviar_estadisticas_clinicas --anio 2026 --mes 6
```
