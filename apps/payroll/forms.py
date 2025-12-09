from django import forms
from .models import Payroll, PayrollEmployee

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['description','year','month','total_amount_services','total_amount','state']


class PayrollEmployeeForm (forms.ModelForm):
      class Meta:
        model = PayrollEmployee
        fields = ['employee','days_worked','total_hours','total_remuneration','total_discounts','net_total']