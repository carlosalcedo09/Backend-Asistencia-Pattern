from django.db import models
from apps.base.models import BaseModel
from apps.employees.models import Employee
from apps.attendance.choices import  StatusChoices,StatusMarkingChoices,StatusJustificationChoices
from apps.schedule.models import Schedule_Detail
from apps.maintenance.models import Type_marking, Type_justification
from datetime import datetime, timedelta, time

class Attendance(BaseModel):
    employee = models.ForeignKey(Employee, db_index=True, verbose_name='Empleado', related_name='empleado_attendance', on_delete=models.CASCADE, null=True)
    date = models.DateField(verbose_name='Fecha de Registro', help_text='Fecha de Registro de Asistencia')
    hours_worked= models.DecimalField(verbose_name='Horas Trabajadas', max_digits=30, decimal_places=2, default=0)
    overtime= models.DecimalField('Horas extra', max_digits=30, decimal_places=2, default=0)
    state = models.CharField(verbose_name="Estado", null=True, blank=True, default="Pendiente", max_length=30, choices=StatusChoices.choices)

    class Meta:
        verbose_name='Asistencia'
        verbose_name_plural= 'Asistencias'
        ordering = ('created_at',)
        unique_together = ('employee', 'date')
        
    def __str__(self):
        return f'{self.employee} - {self.date}'

class Justification(BaseModel):
    attedance = models.ForeignKey(Attendance, db_index=True, verbose_name='Asistencia_Justificacion', related_name='attedance_justification', on_delete=models.CASCADE, null=True)
    reason = models.CharField(verbose_name="Motivo", null=True, blank=True, default=None, max_length=100)
    justification = models.CharField(verbose_name="Justificación", null=True, blank=True, default=None, max_length=300)
    justification_file = models.FileField(upload_to='attendence/templates', null=True, blank=True, verbose_name="Documento de Justificación",
                                     help_text='Evidencias')
    state = models.CharField(verbose_name="Estado", null=True, blank=True, default=None, max_length=30, choices=StatusJustificationChoices.choices)
    type = models.ForeignKey (Type_justification, db_index=True, verbose_name='Tipo de Justificación', help_text= "Establecer el tipo de justificación", related_name='tipo_justificacion', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name='Justificacion'
        verbose_name_plural= 'Justificaciones'
        ordering = ('created_at',)
        
    def __str__(self):
        return f'{self.reason}'

class AttendanceMarking(BaseModel):
    attendance = models.ForeignKey(Attendance, db_index=True, verbose_name='Asistencia', related_name='Asistencia', on_delete=models.CASCADE, null=True)
    hour= models.TimeField(verbose_name='Hora de marcación', null=True,blank=True)
    observation = models.CharField ('Observaciones', help_text="Detallar si existe alguna observación", null=True,blank=True)
    state = models.CharField(verbose_name="Estado", null=True, blank=True, default=None, max_length=30, choices=StatusMarkingChoices.choices)
    type_marking = models.ForeignKey (Type_marking, db_index=True, verbose_name='Tipo de Marcación', help_text= "Establecer el tipo de marcación", related_name='tipo_marcacion', on_delete=models.CASCADE, null=True)

    class Meta: 
        verbose_name = "Marcación"
        verbose_name_plural = "Marcaciones"
        ordering = ('created_at',)
        
    def __str__(self):
        return f'{self.type_marking}'
    
   
    def save(self, *args, **kwargs):
        first_save = not self.pk  

        tipo_actual = self.type_marking.name.upper() if self.type_marking else ""
        asistencia = self.attendance


        if tipo_actual != "INGRESO":
            ingreso_existente = asistencia.Asistencia.filter(type_marking__name__iexact="Ingreso").exists()
            inicio_receso =  asistencia.Asistencia.filter(type_marking__name__iexact="Inicio de Receso").exists()
            salida_existente =  asistencia.Asistencia.filter(type_marking__name__iexact="Salida").exists()

            if not ingreso_existente:
                raise ValueError("No se puede registrar esta marcación sin antes haber registrado un INGRESO.")
            elif tipo_actual=="FIN DE RECESO" and not inicio_receso:
                raise ValueError("No se puede registrar esta marcación sin antes haber registrado un INICIO DE RECESO.")
            elif tipo_actual=="HORAS EXTRA" and not salida_existente:
                raise ValueError("No se puede registrar esta marcación sin antes haber registrado una SALIDA.")


        super().save(*args, **kwargs)

        attendance = self.attendance
        employee = attendance.employee if attendance else None
        fecha = attendance.date if attendance else None
        hora_marcacion = self.hour
        
        asistencias = attendance.Asistencia.all()
        inicio_receso = asistencias.filter(type_marking__name__iexact='Inicio de Receso').order_by('hour').first()
        fin_receso = asistencias.filter(type_marking__name__iexact='Fin de Receso').order_by('hour').first()


        if not (attendance and employee and hora_marcacion):
            return

        hoy = datetime.today()

        # Obtener horario vigente
        horario_detalle = Schedule_Detail.objects.filter(
            employee=employee,
            start_date__lte=fecha,
            end_date__gte=fecha
        ).select_related('schedule').first()

        horario = horario_detalle.schedule if horario_detalle else None

        # === DETERMINAR ESTADO DE LA MARCACIÓN ===
        nuevo_estado = self.state
        if horario:
            tipo = self.type_marking.name.upper()
            hora_actual = datetime.combine(hoy, hora_marcacion)

            if tipo == 'INGRESO':
                hora_entrada = datetime.combine(hoy, horario.check_in_time)
                hora_tolerancia = hora_entrada + horario.tolerance
                nuevo_estado = 'A tiempo' if hora_actual <= hora_tolerancia else 'Fuera de tiempo'

            elif tipo == 'SALIDA':
                nuevo_estado = 'A tiempo' if hora_marcacion >= horario.check_out_time else 'Antes de tiempo'

            elif tipo == 'FIN DE RECESO' or tipo=='INICIO DE RECESO':

                hi_receso = datetime.combine(hoy, inicio_receso.hour) if inicio_receso and inicio_receso.hour else None
                fi_receso = datetime.combine(hoy, fin_receso.hour) if fin_receso and fin_receso.hour else None

                if hi_receso and fi_receso and fi_receso > hi_receso:
                    t_receso = fi_receso - hi_receso
                    if timedelta(hours=1) < t_receso and fi_receso:
                        nuevo_estado = 'Fuera de tiempo'
                    elif timedelta(hours=1) > t_receso and fi_receso:
                        nuevo_estado = 'Antes de tiempo'
                    else: 
                        nuevo_estado = 'A tiempo'
            
                else: 
                        nuevo_estado = 'A tiempo'
            
            elif tipo == 'HORAS EXTRA':
                nuevo_estado = 'No determinado'

            if nuevo_estado != self.state:
                AttendanceMarking.objects.filter(pk=self.pk).update(state=nuevo_estado)
                self.state = nuevo_estado
       
        
        # === CÁLCULO DE HORAS TRABAJADAS Y HORAS EXTRA ===
        if self.type_marking.name.upper() == 'SALIDA':
            entrada = asistencias.filter(type_marking__name__iexact='Ingreso').order_by('hour').first()

            if entrada and entrada.hour and self.hour:
                h_ingreso = datetime.combine(hoy, entrada.hour)
                h_salida = datetime.combine(hoy, self.hour)

                if h_salida < h_ingreso:
                    h_salida += timedelta(days=1)

                if horario:
                    h_salida = min(h_salida, datetime.combine(hoy, horario.check_out_time))

                hi_receso = datetime.combine(hoy, inicio_receso.hour) if inicio_receso and inicio_receso.hour else None
                fi_receso = datetime.combine(hoy, fin_receso.hour) if fin_receso and fin_receso.hour else None

                if hi_receso and fi_receso and fi_receso > hi_receso:
                    t_receso = fi_receso - hi_receso
                    if not timedelta(hours=1) < t_receso < timedelta(hours=3):
                        t_receso = timedelta(hours=1)
                else:
                    t_receso = timedelta(hours=1)

                horas_trabajadas = (h_salida - h_ingreso - t_receso).total_seconds() / 3600
                attendance.hours_worked = round(horas_trabajadas, 2)
                attendance.state = 'Completado'
 
        elif self.type_marking.name.upper() == 'HORAS EXTRA':
            # === CÁLCULO DE HORAS EXTRA ===
            horas_extra = asistencias.filter(type_marking__name__iexact='HORAS EXTRA').order_by('hour')
            if horas_extra.count() >= 2 and horario:
                extra_inicio = horas_extra[0].hour
                extra_fin = horas_extra[1].hour

                h_salida_normal = datetime.combine(hoy, horario.check_out_time)
                h_extra_inicio = datetime.combine(hoy, extra_inicio)
                h_extra_fin = datetime.combine(hoy, extra_fin)

                if (
                    h_extra_inicio > h_salida_normal and
                    h_extra_fin > h_salida_normal and
                    h_extra_fin > h_extra_inicio
                ):
                    print("ENTRE -------------")
                    diferencia_extra = (h_extra_fin - h_extra_inicio).total_seconds() / 3600
                    attendance.overtime = round(diferencia_extra, 2)
                else:
                    attendance.overtime = 0
            else:
                attendance.state = 'Completado'
                attendance.overtime = 0

        else:
                attendance.state = 'En proceso'


        attendance.save(update_fields=['hours_worked', 'state', 'overtime'])