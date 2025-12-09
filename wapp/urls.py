from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .router import endpoints
from apps.api.views import (
    LogoutAllView,
    EmployeeProfileView,
    AttendanceHistoryAPIView,
    HorarioHoyAPIView,
    RegistrarMarcacionAPIView,
    MarcacionesDelDiaAPIView,
    ResumenMarcacionesView,CustomTokenObtainPairView)

from apps.api.dashboard import (
   DashboardResumenGeneralAPIView,
   DashboardTypeMarkingAPIView, 
   DashboardAsistenciasUltimosMeseslAPIView,
   DashboardPuntualidadUltimosMeseslAPIView,
   DashboardAsistenciaAPIView,
   DashboardNominaAPIView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path('management/', TemplateView.as_view(template_name='react/home.html'), name='react-home'),
    path('api/', include(endpoints)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/logout-all/", LogoutAllView.as_view(), name="logout_all"),
    path("api/perfil/", EmployeeProfileView.as_view(), name="employee-profile"),
    path('api/historial/', AttendanceHistoryAPIView.as_view()),
    path("api/horario-hoy/", HorarioHoyAPIView.as_view(), name="horario-hoy"),
    path('api/registrar-marcacion/', RegistrarMarcacionAPIView.as_view(), name='registrar_marcacion'),
    path('api/marcaciones-hoy/', MarcacionesDelDiaAPIView.as_view(), name='marcaciones-hoy'),
    path('api/resumen-hoy/', ResumenMarcacionesView.as_view(), name='resumen-hoy'),
    path("api/dashboard/resumen-general/", DashboardResumenGeneralAPIView.as_view()),
    path("api/dashboard/resumen-mensual-asistencias/", DashboardAsistenciasUltimosMeseslAPIView.as_view()),
    path("api/dashboard/resumen-mensual-puntualidad/", DashboardPuntualidadUltimosMeseslAPIView.as_view()),
    path("api/dashboard/resumen-asistencia/", DashboardAsistenciaAPIView.as_view()),
    path("api/dashboard/resumen-tipo-marcacion/",DashboardTypeMarkingAPIView.as_view()),
    path("api/dashboard/resumen-nomina/", DashboardNominaAPIView.as_view())
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   
"""
import debug_toolbar
urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
]
"""
