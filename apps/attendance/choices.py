from django.db.models import TextChoices

class StatusChoices(TextChoices):
    Pending = 'Pendiente', 'Pendiente'
    In_progress = "En proceso", "En proceso"
    Completed = 'Completado', 'Completado'
    Justified = 'Justificado','Justificado'
   
class StatusMarkingChoices (TextChoices):
    Before_time = 'Antes de tiempo', 'Antes de tiempo'
    On_Time = 'A tiempo', 'A tiempo'
    Lateness = 'Fuera de tiempo', 'Fuera de tiempo'
    Reces = 'No determinado','No determinado'

class StatusJustificationChoices (TextChoices):
    Approved = 'Aprobado', 'Aprobado'
    Rejected = "Rechazado", 'Rechazado'
    Pending = 'Pendiente', 'Pendiente'