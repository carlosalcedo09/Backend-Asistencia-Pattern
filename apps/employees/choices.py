from django.db.models import TextChoices

class DocumentTypeChoices(TextChoices):
    DNI = 'Dni', 'Dni'
    CE = 'Carnet extranjeria', 'Carnet extranjeria'
    PASSPORT = 'Pasaporte', 'Pasaporte'
    EMPTY = '', ''


class SexoChoices(TextChoices):
    M = 'Masculino', 'Masculino'
    F = 'Femenino', 'Femenino'
