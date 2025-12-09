from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_time_in_company(self, employee):
        if not employee.date_entry:
            return "Fecha de ingreso no registrada"

        from datetime import date
        today = date.today()
        delta = today - employee.date_entry
        years = delta.days // 365
        months = (delta.days % 365) // 30

        texto = ""
        if years > 0:
            texto += f"{years} año{'s' if years > 1 else ''} "
        if months > 0:
            texto += f"{months} mes{'es' if months > 1 else ''}"
        return texto.strip() or "Menos de 1 mes"

    def get(self, request):
        user = request.user
        employee = getattr(user, 'employee', None)

        if not employee:
            return Response({"error": "Empleado no encontrado"}, status=404)

        data = {
            "nombre_completo": employee.full_name,
            "cargo": employee.position.name if employee.position else None,
            "personales": {
                "Número de Documento": employee.document_number,
                "Nombre": employee.full_name,
                "Correo": employee.email,
                "Teléfono": employee.cellphone,
                "Género": employee.gender,
            },
            "laborales": {
                "Área": employee.area.name if employee.area else None,
                "Cargo": employee.position.name if employee.position else None,
                "Fecha de ingreso": employee.date_entry,
                "Tipo de pensión": employee.type_pension,
                "Tiempo en la empresa": self.get_time_in_company(employee),
            },
            "ubicacion": {
                "Lugar de marcación": "Sede Central"
            }
        }

        return Response(data)
