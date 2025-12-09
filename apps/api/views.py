# apps/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import status
from apps.attendance.models import AttendanceMarking
from apps.attendance.serializers import AttendanceMarkingSerializer
from django.utils.dateparse import parse_date
from apps.schedule.models import Schedule_Detail
from apps.attendance.models import Type_marking,Attendance
from datetime import date, datetime
from calendar import monthrange
from apps.payroll.calculate_nomina import calculate_employee_data
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"detail": "Sesiones cerradas correctamente."})

class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_time_in_company(self, employee):
        if not employee.date_entry:
            return "Fecha de ingreso no registrada"

        from datetime import date
        today = date.today()
        delta = today - employee.date_entry
        total_days = delta.days

        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        partes = []
        if years > 0:
            partes.append(f"{years} año{'s' if years > 1 else ''}")
        if months > 0:
            partes.append(f"{months} mes{'es' if months > 1 else ''}")
        if days > 0:
            partes.append(f"{days} día{'s' if days > 1 else ''}")

        return " ".join(partes) if partes else "Menos de 1 mes"

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

    def put(self, request):
            employee = getattr(request.user, 'employee', None)
            if not employee:
                return Response({"error": "Empleado no encontrado"}, status=404)

            data = request.data

            personales = data.get('personales', {})
            laborales = data.get('laborales', {})
            ubicacion = data.get('ubicacion', {})

            employee.document_number = personales.get("Número de Documento", employee.document_number)
            employee.full_name = personales.get("Nombre", employee.full_name)
            employee.email = personales.get("Correo", employee.email)
            employee.cellphone = personales.get("Teléfono", employee.cellphone)
            employee.gender = personales.get("Género", employee.gender)

            employee.save()

            return Response({"message": "Datos actualizados correctamente"}, status=status.HTTP_200_OK)
    
class AttendanceHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tipo = request.GET.get("tipo")
        estado = request.GET.get("estado")
        desde = request.GET.get("desde")
        hasta = request.GET.get("hasta")

        qs = AttendanceMarking.objects.filter(attendance__employee__user=user).select_related('type_marking')

        if tipo:
            qs = qs.filter(type_marking__name__iexact=tipo)
        if estado:
            qs = qs.filter(state__iexact=estado)
        if desde:
            qs = qs.filter(attendance__date__gte=parse_date(desde))
        if hasta:
            qs = qs.filter(attendance__date__lte=parse_date(hasta))

        data = AttendanceMarkingSerializer(qs, many=True).data
        return Response(data)
    
class HorarioHoyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee = getattr(user, 'employee', None)
        if not employee:
            return Response({"error": "Empleado no encontrado"}, status=404)

        hoy = date.today()

        detalle = Schedule_Detail.objects.filter(
            employee=employee,
            start_date__lte=hoy,
            end_date__gte=hoy
        ).select_related('schedule').first()

        if not detalle or not detalle.schedule:
            return Response({
                "fecha": hoy.strftime("%d/%m/%Y"),
                "hora_ingreso": "No asignado",
                "hora_salida": "No asignado",
                "tiempo_receso": "No asignado"
            })

        horario = detalle.schedule

        minutos_receso = (
            int(horario.break_time.total_seconds() // 60)
            if horario.break_time else None
        )

        return Response({
            "fecha": hoy.strftime("%d/%m/%Y"),
            "hora_ingreso": horario.check_in_time.strftime("%H:%M") if horario.check_in_time else "No asignado",
            "hora_salida": horario.check_out_time.strftime("%H:%M") if horario.check_out_time else "No asignado",
            "tiempo_receso": f"{minutos_receso} minutos" if minutos_receso is not None else "No asignado"
        })
    
class RegistrarMarcacionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        employee = getattr(user, 'employee', None)

        if not employee:
            return Response({"error": "Empleado no encontrado"}, status=404)
        print(request.data)

        tipo = request.data.get("tipo_marcacion") 
        print(tipo)
        observacion = request.data.get("observacion", "")
        hora_actual = datetime.now().time().replace(microsecond=0)
        hoy = date.today()

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=hoy,
            defaults={"state": "En proceso"}
        )

        try:
            tipo_marcacion = Type_marking.objects.get(name__iexact=tipo)
        except Type_marking.DoesNotExist:
            return Response({"error": "Tipo de marcación no válido"}, status=400)

        marcacion = AttendanceMarking.objects.create(
            attendance=attendance,
            hour=hora_actual,
            observation=observacion,
            type_marking=tipo_marcacion
        )

        return Response({"message": "Marcación registrada correctamente"}, status=status.HTTP_201_CREATED)
    
class MarcacionesDelDiaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee = getattr(user, 'employee', None)

        if not employee:
            return Response({"error": "Empleado no encontrado"}, status=404)

        hoy = date.today()
        marcaciones = AttendanceMarking.objects.filter(
            attendance__employee=employee,
            attendance__date=hoy
        ).order_by('hour')

        serializer = AttendanceMarkingSerializer(marcaciones, many=True)
        return Response(serializer.data)
    
class ResumenMarcacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee = getattr(user, 'employee', None)

        if not employee:
            return Response({"error": "Empleado no encontrado"}, status=404)
        
        
        hoy = datetime.today()
        mes = hoy.month
        anio = hoy.year
        total_tardanzas=0

        total_hours, days_worked, faults,total_horas_extra,dias_restantes = calculate_employee_data(mes, anio, employee)

        _, ultimo_dia = monthrange(anio, mes)
        fecha_inicio = datetime(anio, mes, 1).date()
        fecha_fin = datetime(anio, mes, ultimo_dia).date()

        asistencias = Attendance.objects.filter(
            employee=employee,
            date__range=(fecha_inicio, fecha_fin)
        )

        for asistencia in asistencias:
            marcacion_ingreso = AttendanceMarking.objects.filter(
                attendance=asistencia,
                type_marking__name__iexact='Ingreso'
            ).first()
            if marcacion_ingreso:
                if marcacion_ingreso.state == 'Fuera de tiempo':
                        total_tardanzas += 1
            else: 
                total_tardanzas += 0


        
        if not employee.date_entry:
            return "Fecha de ingreso no registrada"

    
        today = date.today()
        delta = today - employee.date_entry
        total_days = delta.days

        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        partes = []
        if years > 0:
            partes.append(f"{years} año{'s' if years > 1 else ''}"+" ")
        if months > 0:
            partes.append(f"{months} mes{'es' if months > 1 else ''}"+" ")
        if days > 0:
            partes.append(f"{days} día{'s' if days > 1 else ''}"+" ")


        nombre = employee.full_name.split()[0]

        return Response({
            "nombre": nombre,
            "tiempo_empresa":partes,
            "dias_restantes":dias_restantes,
            "asistencias": days_worked,
            "faltas": faults,
            "tardanzas": total_tardanzas,
            "horas_trabajadas": float(total_hours),
            "horas_extra": float(total_horas_extra),
        })


