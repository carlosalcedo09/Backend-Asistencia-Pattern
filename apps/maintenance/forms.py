from django import forms
from .models import Area,Position, Concept, Type_marking,Type_justification,Parameter
from django.utils.safestring import mark_safe


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name','description']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields =['name','description','base_salary']

class ConceptForm(forms.ModelForm):
    class Meta:
        model= Concept
        fields = ['type', 'name','description','is_calculate','formula','start_validity','end_validity']

    class Media:
        js = ('admin/js/concept_formula.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        conceptos = Concept.objects.all().order_by('name')
        parametros = Parameter.objects.all().order_by('name')

        concept_options = ''.join([
            f'<option value="[{c.name}]">{c.name}</option>'
            for c in conceptos
        ])

        param_options = ''.join([
            f'<option value="[{p.name}]">{p.name}</option>'
            for p in parametros
        ])

        html_help = f"""
        <label><b>Insertar concepto:</b></label>
        <select id="concept-selector">
            <option value="">-- Seleccionar concepto --</option>
            {concept_options}
        </select>

        <label style="margin-left: 20px;"><b>Insertar parámetro:</b></label>
        <select id="param-selector">
            <option value="">-- Seleccionar parámetro --</option>
            {param_options}
        </select>
        """

        self.fields['formula'].help_text = mark_safe(html_help) 

class TypeMarkingForm(forms.ModelForm):
    class Meta:
        model= Type_marking
        fields = ['name','description']

class Type_justificationForm(forms.ModelForm):
    class Meta:
        model= Type_justification
        fields = ['name','description']
