from django.db import models
from apps.base.models import BaseModel
from apps.maintenance.choices import ConceptType, ParameterType,YEARS
from django.core.exceptions import ValidationError
    

class Area (BaseModel):
    name = models.CharField('Nombre', max_length=250, help_text='Nombre de Area')
    description = models.CharField('Descripción', max_length=250, help_text='Descripción de Área', null=True)
    
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name}'  

class Position (BaseModel):
    name = models.CharField('Cargo', max_length=250, help_text='Nombre de Cargo')
    description= models.CharField('Descripción', max_length=250, help_text='Descripción del cargo', null=True)
    base_salary= models.DecimalField('Salario Base', max_digits=30, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name}'  
    
class Concept (BaseModel):
    type = models.CharField('Tipo', max_length=30, choices=ConceptType.choices, default=ConceptType.base)
    name = models.CharField('Nombre', max_length=250, help_text='Nombre de Concepto')
    description = models.CharField('Descripción', max_length=200, null=True,blank=True, help_text='Descripción de concepto de nómina')
    is_calculate = models.BooleanField('¿Es calculable?', default=True)
    formula = models.TextField('Formula', null=True, blank=True)
    start_validity = models.CharField('Año inicio', max_length=4, choices=YEARS)
    end_validity = models.CharField('Año fin', max_length=4, choices=YEARS)

    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name}'

class Parameter(BaseModel):
    name = models.CharField('Nombre', max_length=30, null=True)
    code = models.CharField('Código', max_length=10,unique=True, null=True, blank=True)
    description = models.CharField('Descripción', max_length=250, null=True, blank=True)
    concept = models.ForeignKey(Concept, verbose_name='Concepto', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Parametro'
        verbose_name_plural = 'Parametros'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name} - {self.code}'
    
    
    def save(self, *args, **kwargs):
        if self.code is None:
            last_parameterDescription = Parameter.objects.all().order_by('code').last()

            if last_parameterDescription:
                last_code = int(last_parameterDescription.code)
                new_code = str(last_code + 1).zfill(3)
            else:
                new_code = "001"
            self.code = new_code

        super(Parameter, self).save(*args, **kwargs)

class ParameterHistory(BaseModel):
    type = models.CharField('Tipo', choices=ParameterType.choices, max_length=10, default=ParameterType.decimal)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Parametro')
    value = models.DecimalField('Valor Decimal', max_digits=15, decimal_places=6, default=0, blank=True,
                                help_text='Valor decimal del parametro registado en el sistema')
    date = models.DateField('Valor Fecha', null=True, blank=True)
    start_validity = models.CharField('Año inicio', max_length=4, choices=YEARS)
    end_validity = models.CharField('Año fin', max_length=4, choices=YEARS)

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historial'
        ordering = ('-end_validity',)

    def __str__(self):
        return f'{self.start_validity} - {self.end_validity}'
    
    def save(self, *args, **kwargs):
        if self.type == ParameterType.date: self.value = 0
        else: self.date = None
        super(ParameterHistory, self).save(*args, **kwargs)

    def clean(self):
        if self.start_validity and self.end_validity and int(self.start_validity) > int(self.end_validity):
            raise ValidationError({
                'start_validity': 'El año inicio no puede ser mayor que el año fin'
            })
        if self.type == ParameterType.date and self.date is None:
            raise ValidationError({'date': 'Es requerido este campo'})
        elif self.type == ParameterType.decimal and self.value is None:
            raise ValidationError({'value': 'Es requerido este campo'})


        overlapping_configs = ParameterHistory.objects.filter(
            parameter=self.parameter,
            start_validity__lte=self.end_validity,
            end_validity__gte=self.start_validity
        ).exclude(pk=self.pk)

        if overlapping_configs.exists():
            raise ValidationError({
                'start_validity': 'El rango de fechas se cruza con otro registro existente'
            })

        previous_config = ParameterHistory.objects.filter(
            parameter=self.parameter,
            start_validity__lte=self.start_validity
        ).exclude(pk=self.pk) 
        previous_config = previous_config.order_by('-end_validity').first() 

        if previous_config:
            expected_start = int(previous_config.end_validity) + 1
            if int(self.start_validity) != expected_start:
                raise ValidationError({
                    'start_validity': 'El año inicio debe ser un año después del año fin del registro anterior: {expected}.'.format(expected=expected_start)
                })
            
        super().clean()

class Type_marking(BaseModel):
    name = models.CharField('Nombre', max_length=200, null=True, unique=True, help_text='Nombre de tipo de marcación')
    description = models.CharField('Descripción', max_length=200, null=True,blank=True, help_text='Descripción de tipo de marcación')
     
    class Meta:
        verbose_name = 'Tipo de Marcación'
        verbose_name_plural = 'Tipo de marcaciones'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name}'

class Type_justification(BaseModel):
    name = models.CharField('Nombre', max_length=200, null=True, unique=True, help_text='Nombre de tipo de justificación')
    description = models.CharField('Descripción', max_length=200, null=True,blank=True, help_text='Descripción de tipo de justificación')

    class Meta:
        verbose_name = 'Tipo de justificación'
        verbose_name_plural = 'Tipo de justificaciones'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.name}'
