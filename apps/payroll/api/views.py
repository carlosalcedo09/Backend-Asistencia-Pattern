from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db import connection
from django.db.models import Prefetch

from apps.payroll.models import Payroll, PayrollEmployee, PayrrollEmployeeDetail
from apps.maintenance.models import Concept


class PayrollViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = []

    @action(detail=False, methods=['get'])
    def payroll_preview(self, request):
        payroll_id = request.query_params.get('payroll')
        if not payroll_id:
            return Response({'message': 'Es requerido el ID de la nómina'}, status=400)

        payroll = Payroll.objects.filter(id=payroll_id).first()
        if not payroll:
            return Response({'message': 'Nómina no encontrada'}, status=404)

        # Obtener empleados y conceptos asociados
        employees = PayrollEmployee.objects.filter(payroll=payroll).prefetch_related(
            Prefetch(
                'Nomina_Empleado',
                queryset=PayrrollEmployeeDetail.objects.select_related('concept'),
                to_attr='concept_details'
            ),
            'employee__position',
            'employee'
        )

        header_concepts = set()
        employee_data = []

        for emp in employees:
            details = []
            for detail in emp.concept_details:
                concept_name = detail.concept.name
                header_concepts.add(concept_name)
                details.append({
                    'concept': concept_name,
                    'value': float(detail.calculated_amount)
                })

            employee_data.append({
                'employee_doc': emp.employee.document_number if emp.employee else '',
                'employee_name': emp.employee.full_name if emp.employee else '',
                'employee_entry': emp.employee.date_entry if emp.employee else '',
                'area': emp.employee.area.name if emp.employee and emp.employee.area else '',
                'position': emp.employee.position.name if emp.employee and emp.employee.position else '',
                'concepts': details
            })

        return Response({
            'description': payroll.description,
            'year': payroll.year,
            'month': payroll.month,
            'total': float(payroll.total_amount),
            'header_concepts': list(header_concepts),
            'employees': employee_data
        })
