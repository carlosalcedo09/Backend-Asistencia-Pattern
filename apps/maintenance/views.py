from django.contrib import messages
from apps.maintenance.models import Area
from apps.base.views import ( decode_xls_file, validate_columns, process_xls_rows,export_data)
import os


def process_area(request):
    xls_file = request.FILES["xls_file"]  
    
    file_extension = os.path.splitext(xls_file.name)[1]
    if file_extension not in ['.xls', '.xlsx']:
        messages.error(request, f"Formato de archivo no soportado: {file_extension}. Solo se permiten archivos .xls o .xlsx.")
        return

    header, rows, error = decode_xls_file(xls_file)
    if error:
        messages.error(request, error)
        return

    expected_columns = ['Nombre de Área', 'Descripción']
    
    valid, error_msg = validate_columns(header, expected_columns)
    if not valid:
        messages.error(request, error_msg)
        return

    rows, error_msg = process_xls_rows(rows, len(expected_columns))
    if not rows:
        messages.error(request, error_msg)
        return

    for row in rows:
        name, description = row
        if not  name or not description:
            messages.error(request, f"Todos los campos son requeridos en la fila: {row}")
            continue
        if not Area.objects.filter(name=name).exists():
            Area.objects.create(name=name, description=description)
    messages.success(request, "Archivo Excel procesado exitosamente.")

def export_area(request):
    areas = Area.objects.all()
    headers = ['Nombre de Área', 'Descripción']
    data = [[
        area.name,
        area.description
    ] for area in areas]
    return export_data(request, 'Area', headers, data, 'Consolidado_Areas.xlsx')

