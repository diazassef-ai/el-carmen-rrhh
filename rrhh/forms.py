from django import forms

from .models import AgendaClinicaMovil, DocumentoAdjunto, Funcionario, PermisoCapacitacion


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            field.widget.attrs["class"] = field.widget.attrs.get("class", css_class)


class FuncionarioForm(BootstrapModelForm):
    class Meta:
        model = Funcionario
        fields = [
            "rut",
            "nombre_completo",
            "cargo",
            "tipo_contrato",
            "unidad",
            "correo_electronico",
            "activo",
        ]


class PermisoCapacitacionForm(BootstrapModelForm):
    class Meta:
        model = PermisoCapacitacion
        fields = [
            "funcionario",
            "tipo_solicitud",
            "numero_dias",
            "fecha_desde",
            "fecha_hasta",
            "hora_desde",
            "hora_hasta",
            "dias_pendientes",
            "observaciones",
            "fecha_entrega_solicitante",
            "fecha_recepcion_oficina_personal",
            "estado",
            "nombre_capacitacion",
            "institucion_organizadora",
            "modalidad",
            "lugar",
            "observaciones_capacitacion",
        ]
        widgets = {
            "fecha_desde": forms.DateInput(attrs={"type": "date"}),
            "fecha_hasta": forms.DateInput(attrs={"type": "date"}),
            "hora_desde": forms.TimeInput(attrs={"type": "time"}),
            "hora_hasta": forms.TimeInput(attrs={"type": "time"}),
            "fecha_entrega_solicitante": forms.DateInput(attrs={"type": "date"}),
            "fecha_recepcion_oficina_personal": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
            "observaciones_capacitacion": forms.Textarea(attrs={"rows": 3}),
        }


class DocumentoAdjuntoForm(BootstrapModelForm):
    class Meta:
        model = DocumentoAdjunto
        fields = ["archivo", "nombre"]


class AgendaClinicaMovilForm(BootstrapModelForm):
    class Meta:
        model = AgendaClinicaMovil
        fields = [
            "clinica",
            "fecha",
            "hora_inicio",
            "hora_termino",
            "lugar",
            "sector",
            "cupos_totales",
            "cupos_reservados",
            "responsable",
            "estado",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_termino": forms.TimeInput(attrs={"type": "time"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }


class ReporteExcelForm(forms.Form):
    mes = forms.IntegerField(min_value=1, max_value=12, required=False)
    anio = forms.IntegerField(label="Ano", min_value=2020, max_value=2100, required=False)
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(),
        required=False,
        empty_label="Todos los funcionarios",
    )
    unidad = forms.CharField(required=False)
    tipo_solicitud = forms.ChoiceField(
        choices=[("", "Todos los tipos")] + PermisoCapacitacion.TIPOS_SOLICITUD,
        required=False,
    )
    tipo_contrato = forms.ChoiceField(
        choices=[("", "Todos los contratos")] + Funcionario.TIPOS_CONTRATO,
        required=False,
    )
    estado = forms.ChoiceField(
        choices=[("", "Todos los estados")] + PermisoCapacitacion.ESTADOS,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
