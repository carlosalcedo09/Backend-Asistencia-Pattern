from django.contrib import admin
from apps.payroll.forms import PayrollForm, PayrollEmployeeForm
from django.http import HttpResponseRedirect,HttpResponse
from apps.maintenance.models import Concept
from apps.maintenance.choices import ConceptType, StatusPayrrolChoices
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from apps.subadmin import  SubAdmin,RootSubAdmin
from apps.payroll.models import PayrollEmployee, Payroll, PayrrollEmployeeDetail
from apps.payroll.calculate_nomina import generate_payroll_data 
from django.contrib import messages
from apps.payroll.utils import export_payroll_excel_response,export_payroll_boleta_response
from unfold.decorators import display

from django.shortcuts import get_object_or_404

class PayrollEmployeeDetailInLIne(admin.TabularInline):
    model = PayrrollEmployeeDetail
    extra = 0
    exclude = ('state', 'creator_user', 'deleted_at','deleted_user','modified_user','modified_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'concept':
            kwargs['queryset'] = Concept.objects.filter(type__in=[ConceptType.base, ConceptType.auxiliary, ConceptType.discount])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PayrollEmployeeSubAdmin(SubAdmin):
    model = PayrollEmployee
    list_display =  ('employee','days_worked','total_hours','total_remuneration','net_total','edit','payrollemployee')
    list_display_links = ('edit',)
    search_fields = ['employee']
    inlines = [PayrollEmployeeDetailInLIne]
    list_per_page = 10
    form=PayrollEmployeeForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    edit.short_description = '->'

    def payrollemployee(self, obj):
        url = reverse('admin:payroll_payrollemployee_export_boleta', args=[obj.id])
        return format_html('<a class="button download-report-btn" href="{}" target="_blank">Descargar</a>', url)
    payrollemployee.short_description = 'Boleta de Pago'



    
class PayrollAdmin (RootSubAdmin):
    list_display = ('description','year','month','total_amount','show_status_customized_color','edit','payroll')
    list_display_links = ('edit',)
    search_fields = ['description']
    list_per_page = 15
    form=PayrollForm
    subadmins = [PayrollEmployeeSubAdmin]
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'
    
    def payroll(self, obj):
        if obj.state == StatusPayrrolChoices.Review:
                return format_html('''
                    <button type="button" class="button generate-payroll-btn" data-id="{}">Revisar</button>
                    <a class="button download-report-btn" href="{}">Exportar</a> ''',
                obj.id,
                reverse('admin:payroll_export_excel', args=[obj.id])
                )
        elif obj.state == StatusPayrrolChoices.Approved:
            return format_html(
                   '''<a class="button download-report-btn" href="{}">Exportar</a> ''',
                reverse('admin:payroll_export_excel', args=[obj.id])
                )
        return '-'
    payroll.short_description = 'Acciones'

    def get_urls(self):
            urls = super().get_urls()
            my_urls = [
                path('<uuid:id>/payroll/', self.admin_site.admin_view(self._confirmed_payroll), name='payroll'),
                path('<uuid:id>/export_excel/', self.admin_site.admin_view(self.export_payroll_to_excel), name='payroll_export_excel'),
                path('<uuid:id>/payroll/', self.admin_site.admin_view(self._confirmed_payroll), name='payroll'),
                path('payrollemployee/<uuid:id>/export/', self.admin_site.admin_view(self.export_boleta),name='payroll_payrollemployee_export_boleta')
            ]
            return my_urls + urls
    
    def _confirmed_payroll(self, request, id):
        payroll = Payroll.objects.filter(pk=id).first()
        if not payroll:
            return HttpResponse("Nómina no encontrada", status=404)
        payroll.state = StatusPayrrolChoices.Approved
        payroll.save()
        return HttpResponse("Nómina aprobada")
    
    def export_payroll_to_excel(self, request, id):
        try:
            payroll = Payroll.objects.get(id=id)
            return export_payroll_excel_response(payroll)
        except Payroll.DoesNotExist:
            messages.error(request, "La nómina no fue encontrada.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al generar el Excel: {str(e)}")
        
        return redirect('/admin/payroll/payroll/')

    def export_boleta(self, request, id):
        try:
            payroll_employee = PayrollEmployee.objects.get(id=id)
            return export_payroll_boleta_response(payroll_employee)
        except PayrollEmployee.DoesNotExist:
            messages.error(request, "La boleta no fue encontrada.")
        except Exception as e:
            messages.error(request, f"Error exportando boleta: {str(e)}")
        
        payroll_id = payroll_employee.payroll.id if 'payroll_employee' in locals() else ''
        return redirect(f'/admin/payroll/payroll/{payroll_id}/payrollemployee/')



    class Media:
        js = ('admin/js/hide_view.js',)
    
    @display(
        description="Estado",
        ordering="state",
        label={
            StatusPayrrolChoices.Rejected: "warning",
            StatusPayrrolChoices.Approved: "success",
            StatusPayrrolChoices.Review: "dark",
        },
    )

    def show_status_customized_color(self, obj):
        return obj.state

    def save_model(self, request, obj, form, change):

        if Payroll.objects.filter(year=obj.year, month=obj.month).exclude(pk=obj.pk).exists():
            messages.error(request, " Ya existe una nómina para ese año y mes.")
            self._cancel_save = True
            return

        is_new = not change  
        super().save_model(request, obj, form, change)

        if is_new:
            generate_payroll_data(obj)
            messages.success(request, "Nómina por empleado generada con éxito")

    def response_add(self, request, obj, post_url_continue=None):
        if hasattr(self, '_cancel_save') and self._cancel_save:
            # Redirige sin mostrar el mensaje de éxito del admin
            return HttpResponseRedirect(reverse('admin:payroll_payroll_changelist'))
        return super().response_add(request, obj, post_url_continue)

admin.site.register(Payroll, PayrollAdmin)