from django.contrib import admin

from .models import DocumentoAdjunto, Funcionario, PermisoCapacitacion


class DocumentoAdjuntoInline(admin.TabularInline):
    model = DocumentoAdjunto
    extra = 1


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre_completo", "cargo", "unidad", "tipo_contrato", "activo")
    list_filter = ("unidad", "tipo_contrato", "activo")
    search_fields = ("rut", "nombre_completo", "cargo", "unidad")


@admin.register(PermisoCapacitacion)
class PermisoCapacitacionAdmin(admin.ModelAdmin):
    list_display = ("funcionario", "tipo_solicitud", "fecha_desde", "fecha_hasta", "numero_dias", "estado")
    list_filter = ("tipo_solicitud", "estado", "fecha_desde", "funcionario__unidad")
    search_fields = ("funcionario__rut", "funcionario__nombre_completo", "funcionario__cargo", "funcionario__unidad")
    inlines = [DocumentoAdjuntoInline]


@admin.register(DocumentoAdjunto)
class DocumentoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "solicitud", "subido_en")
    search_fields = ("nombre", "solicitud__funcionario__nombre_completo")
