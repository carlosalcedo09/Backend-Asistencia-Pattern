from django.db import models
import uuid
from django.utils import timezone
from apps.base.middleware import get_current_employee


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Registrado el', auto_now_add=True)
    updated_at = models.DateTimeField('Ultima actualización', auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField('Fecha y hora de eliminacion',null=True, blank=True)
    deleted_user = models.ForeignKey('employees.Employee', null=True, blank=True, on_delete=models.SET_NULL, related_name="deleted_%(class)s")
    modified_user = models.ForeignKey('employees.Employee', null=True, blank=True, on_delete=models.SET_NULL, related_name="modified_%(class)s")
    creator_user = models.ForeignKey('employees.Employee', verbose_name='Usuario creador', on_delete=models.CASCADE, null=True, blank=True, related_name="created_%(class)s")
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    state = models.BooleanField('Estado', null=True, blank=True, default=False)
    
    def save(self, *args, **kwargs):
        user = get_current_employee()
        if user and not kwargs.pop('disable_user_tracking', False):
            self.modified_user = user
        super().save(*args, **kwargs)
        
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.deleted_user = get_current_employee() 
        self.state = False 
        self.save()
        
    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'
        ordering = ['-created_at']
