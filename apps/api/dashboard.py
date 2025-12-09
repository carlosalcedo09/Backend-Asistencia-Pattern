from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.api.services import get_dashboard_asistencia, get_dashboard_nomina,get_dashboard_ultimosmeses,get_dashboard_ultimosmesespuntualidad,get_dashboard_mesasistenciaarea,get_dashboard_mestype_marking
from datetime import datetime

class DashboardResumenGeneralAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_asistencia(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DashboardAsistenciasUltimosMeseslAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_ultimosmeses(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DashboardPuntualidadUltimosMeseslAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_ultimosmesespuntualidad(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DashboardAsistenciaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_mesasistenciaarea(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DashboardTypeMarkingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_mestype_marking(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class DashboardNominaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))
        month = int(request.GET.get("month", datetime.now().month))

        try:
            data = get_dashboard_nomina(year, month)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)