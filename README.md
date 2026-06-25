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
5. Cuando termine el deploy, abrir la Shell de Render y crear el primer administrador:

```bash
python manage.py createsuperuser
```

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

## Seguridad de sesion

La plataforma cierra la sesion por inactividad a nivel servidor y navegador. Al usar "Cerrar sesion" en una ventana, las demas pestanas abiertas detectan el cierre y vuelven al login.
