from django.db.models import TextChoices

class StatusPayrrolChoices(TextChoices):
    Approved = 'Aprobado', 'Aprobado'
    Rejected = "Rechazado", 'Rechazado'
    Review = 'En revisión', 'En Revisión'


class Months(TextChoices):
    January = 'Enero', 'Enero'
    February = 'Febrero', 'Febrero'
    March = 'Marzo', 'Marzo'
    April = 'Abril', 'Abril'
    May = 'Mayo', 'Mayo'
    June = 'Junio', 'Junio'
    July = 'Julio', 'Julio'
    August = 'Agosto', 'Agosto'
    September = 'Septiembre', 'Septiembre'
    October = 'Octubre', 'Octubre'
    November = 'Noviembre', 'Noviembre'
    December = 'Diciembre', 'Diciembre'

class ParameterType(TextChoices):
    decimal = 'decimal', 'Decimal'
    date = 'fecha', 'Fecha'
    
class ConceptType(TextChoices):
    base = 'base', 'Concepto Base'
    discount = 'descuento', 'Concepto de Descuento'
    auxiliary = 'auxiliar', 'Concepto Auxiliar'

YEARS = [(str(r), str(r)) for r in range(2024, 2051)]