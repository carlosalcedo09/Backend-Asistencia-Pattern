from rest_framework import routers
from apps.payroll.api.views import PayrollViewSet

router = routers.DefaultRouter()
router.include_root_view = False


urlpatterns = router.urls
router.register('payroll', PayrollViewSet, basename='payroll')
endpoints = router.urls