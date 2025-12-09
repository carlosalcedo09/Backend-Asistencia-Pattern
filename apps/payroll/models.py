from django.db import models
from apps.base.models import BaseModel
from apps.maintenance.choices import ConceptType, ParameterType,YEARS
from django.core.exceptions import ValidationError
from apps.employees.models import Employee
from apps.maintenance.models import Concept
from apps.maintenance.choices import Months,StatusPayrrolChoices
    

class Payroll (BaseModel):
    description = models.CharField('Descripción', max_length=250, help_text='Descripción de la Nómina', null=True)
    year= models.CharField('Ejercicio', max_length=4, help_text='Año de aplicación para la planificación registrada')
    month= models.CharField(verbose_name="Mes", null=True, default=None, max_length=30, choices=Months.choices)
    total_amount_services= models.DecimalField('Monto total por servicios',null=True, blank=True, max_digits=30, decimal_places=5, default=0)
    total_amount= models.DecimalField('Monto Total', null=True, blank=True,max_digits=30, decimal_places=5, default=0)
    state = models.CharField(verbose_name="Estado", null=True, blank=True, default=None, max_length=30, choices=StatusPayrrolChoices.choices)

    class Meta:
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nómina'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.description}'  

class PayrollEmployee (BaseModel):
    payroll = models.ForeignKey(Payroll, db_index=True, verbose_name='Nomina', related_name='Nomina', on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee,  db_index=True, verbose_name='Empleado', null=True, on_delete=models.CASCADE, related_name='budget_employee', help_text='Código y nombre del empleado')
    days_worked = models.IntegerField(verbose_name="Total de días laborados",null=True, blank=True,)
    faults= models.IntegerField(verbose_name="Faltas",null=True, blank=True,)
    total_hours = models.DecimalField('Total de horas laboradas', max_digits=30, decimal_places=2, default=0)
    overtime = models.DecimalField('Horas extra laboradas', max_digits=30, decimal_places=2, default=0)
    total_remuneration= models.DecimalField('Total remuneración', max_digits=30, decimal_places=3, default=0)
    total_discounts = models.DecimalField('Total de descuentos', max_digits=30, decimal_places=3, default=0)
    total_amount_services = models.DecimalField('Total aportes empleador', max_digits=30, decimal_places=3, default=0)
    net_total = models.DecimalField('Total neto', max_digits=30, decimal_places=3, default=0)

    class Meta:
        verbose_name = 'Nomina Empleado'
        verbose_name_plural = 'Nominas Empleados'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.employee}'

class PayrrollEmployeeDetail(BaseModel):
    payroll_employee = models.ForeignKey(PayrollEmployee, db_index=True, verbose_name='Nomina Empleado', related_name='Nomina_Empleado', on_delete=models.CASCADE, null=True)
    concept = models.ForeignKey(Concept, db_index=True, on_delete=models.CASCADE, verbose_name='Concepto')
    calculated_amount = models.DecimalField('Monto calculado', max_digits=30, decimal_places=5, default=0)

    class Meta:
        verbose_name = 'Concepto nómina'
        verbose_name_plural = 'Conceptos nómina'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.payroll_employee}'