from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="rrhh_dashboard"),
    path("funcionarios/", views.funcionarios_lista, name="rrhh_funcionarios"),
    path("funcionarios/nuevo/", views.funcionario_crear, name="rrhh_funcionario_crear"),
    path("funcionarios/<int:pk>/", views.funcionario_ficha, name="rrhh_funcionario_ficha"),
    path("funcionarios/<int:pk>/editar/", views.funcionario_editar, name="rrhh_funcionario_editar"),
    path("solicitudes/", views.solicitudes_lista, name="rrhh_solicitudes"),
    path("solicitudes/nueva/", views.solicitud_crear, name="rrhh_solicitud_crear"),
    path("solicitudes/<int:pk>/", views.solicitud_detalle, name="rrhh_solicitud_detalle"),
    path("solicitudes/<int:pk>/editar/", views.solicitud_editar, name="rrhh_solicitud_editar"),
    path("solicitudes/<int:pk>/anular/", views.solicitud_anular, name="rrhh_solicitud_anular"),
    path("solicitudes/<int:pk>/adjuntar/", views.adjunto_crear, name="rrhh_adjunto_crear"),
    path("calendario/", views.calendario, name="rrhh_calendario"),
    path("calendario/visualizacion/", views.calendario_visualizacion, name="rrhh_calendario_visualizacion"),
    path("calendario/eventos/", views.calendario_eventos, name="rrhh_calendario_eventos"),
    path("ausentes-hoy/", views.ausentes_hoy, name="rrhh_ausentes_hoy"),
    path("reportes/", views.reportes_excel, name="rrhh_reportes"),
    path("buscar/", views.busqueda_global, name="rrhh_busqueda"),
]
