from django.db import models
from apps.base.models import BaseModel
from apps.employees.models import Employee

    
class Schedule(BaseModel):
    description= models.CharField('Descripción', max_length=250, help_text='Descripción del cargo', null=True)
    check_in_time= models.TimeField('Hora de ingreso',help_text='Detallar hora de ingreso a laborar', null=True)
    check_out_time= models.TimeField('Hora de salida',help_text='Detallar hora de salida de laborar', null=True)
    tolerance = models.DurationField('Tolerancia', help_text='Tiempo de tolerancia al ingreso (ej: 5 minutos)', null=True, blank=True)
    break_time = models.DurationField('Tiempo de receso', help_text='Duración del receso (ej: 1 hora)', null=True, blank=True)
    working_days= models.IntegerField('Días laborales', help_text='', null=True)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.description}'
    

class Schedule_Detail(BaseModel):
    employee=  models.ForeignKey(Employee, db_index=True, verbose_name='Empleado', related_name='Empleado', on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, db_index=True, verbose_name='Horario', related_name='Horario', on_delete=models.CASCADE, null=True)
    start_date=  models.DateField(verbose_name='Fecha de Inicio de Vigencia', help_text='Fecha de Inicio de Vigencia')
    end_date =  models.DateField(verbose_name='Fecha de Fin de Vigencia', help_text='Fecha de Fin de Vigencia')

    class Meta:
        verbose_name = 'Detalle de Horario'
        verbose_name_plural = 'Detalles de Horarios'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.schedule}-{self.employee}'
