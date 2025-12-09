from collections import defaultdict
from django.db import models
from datetime import date
from apps.base.models import BaseModel
from apps.employees.choices import  DocumentTypeChoices, SexoChoices
from apps.maintenance.models import Area, Position
from apps.users.models import User

class Employee(BaseModel):
    document_type = models.CharField(verbose_name="Tipo de documento", default=None, null=True, blank=True, max_length=30, choices=DocumentTypeChoices.choices)
    document_number = models.CharField('Código', max_length=10)
    profile_picture= models.FileField(upload_to='employee/templates', null=True, blank=True, verbose_name="Foto de Perfil",
                                     help_text='Subir la imagen (jpg,jpge, png)')
    full_name = models.CharField(verbose_name='Nombre completo', max_length=200, null=True)
    email = models.EmailField(verbose_name='Correo Electrónico',max_length = 50, null=True, blank=True)
    cellphone = models.CharField(verbose_name='Celular', max_length=15, null=True, blank=True)
    gender = models.CharField(verbose_name="Sexo", null=True, blank=True, default=None, max_length=30, choices=SexoChoices.choices)
    has_children= models.BooleanField(verbose_name="¿Tiene Hijos?", default = False) 
    area=  models.ForeignKey(Area, db_index=True, verbose_name='Área', related_name='Area', on_delete=models.CASCADE, null=True)
    position=  models.ForeignKey(Position, db_index=True, verbose_name='Cargo', related_name='Cargo', on_delete=models.CASCADE, null=True )
    is_active = models.BooleanField(default = True) 
    date_entry = models.DateField(verbose_name='Fecha de Ingreso', help_text='Fecha de ingreso de empleado')
    code_afp = models.CharField(verbose_name='Código de AFP', max_length=200, null=True)
    type_pension = models.CharField(verbose_name="Tipo de pensión", null=True, blank=True, default=None, max_length=50)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='employee')

    
    created = models.DateTimeField('Se unió el', auto_now_add=True)
    updated = models.DateTimeField('Ultima actualización', auto_now=True)
    
    class Meta:
        verbose_name='Empleado'
        verbose_name_plural= 'Empleados'
        ordering = ('created_at',)
        
    def __str__(self):
        return f'{self.document_number} - {self.full_name}'
    

    
    def get_time_in_company(self):
        if self.date_entry:
            today = date.today()
            delta = today - self.date_entry
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} años, {months} meses"
        
        return "Fecha de ingreso no disponible"
    