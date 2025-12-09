from django.contrib import admin
from .models import Employee
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect
from apps.employees.views import  export_employee
from apps.subadmin import RootSubAdmin, SubAdmin
from apps.employees.forms import EmployeeForm

    
    
class EmployeeAdmin(RootSubAdmin):
    list_display=('document_number', 'full_name', 'area','position','date_entry', 'edit',)
    list_display_links=('edit', 'document_number', 'full_name', 'date_entry')
    search_fields=('document_number', 'full_name',)
    list_filter=['area','position']
    exclude = ['is_active', 'state', 'creator_user',]
    change_list_template = "admin/upload_employee.html"
    form = EmployeeForm
    
    class Media:
        js = ('admin/js/employee_position.js',) 
        
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'
        
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-employee/', self.admin_site.admin_view(self.upload_xls), name='upload_employee'),
            path('export-employee/', self.admin_site.admin_view(self.export_xls), name='export_employee')
        
        ]
        return my_urls + urls

    def upload_xls(self, request):
        if request.method == "POST" and request.FILES.get('xls_file'):
            #process_employee(request)
            return redirect(reverse('admin:employees_employee_changelist'))
        return render(request, 'admin/upload_employee.html')
    
    def export_xls(self,request):
        return export_employee(request)
    
admin.site.register(Employee, EmployeeAdmin)
