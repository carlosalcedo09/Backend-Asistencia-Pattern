from django.contrib import admin
from apps.base.admin import BaseAdmin
from apps.maintenance.models import Area,Position,Concept,ParameterHistory,Parameter, Type_marking, Type_justification
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from apps.maintenance.views import process_area,export_area
from apps.maintenance.forms import AreaForm, ConceptForm,TypeMarkingForm,PositionForm,Type_justificationForm

class AreaAdmin (BaseAdmin):
    list_display = ('name','description','edit')
    list_display_links = ('edit',)
    search_fields = ['name']
    list_per_page = 15
    change_list_template = "admin/upload_area.html"
    form=AreaForm
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'
    
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-area/', self.admin_site.admin_view(self.upload_xls), name='upload_area'),
            path('export-area/', self.admin_site.admin_view(self.export_xls), name='export_area')
        ]
        return my_urls + urls

    def upload_xls(self, request):
        if request.method == "POST" and request.FILES.get('xls_file'):
            process_area(request) 
            return redirect('admin:maintenance_area_changelist')  
        return render(request, 'admin/upload_area.html')
    
    def export_xls(self,request):
        return export_area(request)

class PositionAdmin(BaseAdmin):
    list_display = ('name','description','base_salary','edit')
    list_display_links = ('edit',)
    search_fields = ['name']
    list_per_page = 15
    form=PositionForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

class ConceptAdmin (BaseAdmin):
    list_display = ('type','name','description','is_calculate','edit')
    list_display_links = ('edit',)
    search_fields = ['name','is_calculate']
    list_filter=['type']
    list_per_page = 15
    #change_list_template = "admin/upload_area.html"
    form=ConceptForm
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

class ParameterHistoryInline(admin.TabularInline):
    model = ParameterHistory
    extra = 0
    #classes = ('collapse',)
    exclude = ('state','created_at','updated_at','deleted_at','deleted_user','creator_user','modified_user')

    class Media:
        js = ('admin/js/parameter.js',)

class ParameterAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'description','concept','edit')
    list_display_links = ('edit',)
    search_fields = ('name',)
    inlines = [ParameterHistoryInline]
    list_per_page = 20
    exclude = ('creator_user', 'state')
    fieldsets = (
        (None, {
            'fields': ('name', 'description','concept')
        }),
    )
    
    class Media:
        js = ('admin/js/hide_view.js',)

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'
    

    # def value_date(self, obj):
    #     if obj.type == ParameterType.decimal:
    #         val = float(str(obj.value).replace(',','.'))
    #         if val.is_integer(): val=str(int(val))
    #         if obj.denominator == 1: return f'{val}'
    #         else: return f'{val}/{obj.denominator}'
    #     else: return obj.date
    # value_date.short_description = 'Valor'

    def save_model(self, request, obj, form, change):
        if not change and not obj.creator_user and hasattr(request.user, 'employee'):
            obj.creator_user = request.user.employee
        super().save_model(request, obj, form, change)


class Type_markingAdmin (BaseAdmin):
    list_display = ('name','description','edit')
    list_display_links = ('edit',)
    search_fields = ['name']
    list_per_page = 15
    #change_list_template = "admin/upload_area.html"
    form=TypeMarkingForm
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

class Type_justificationAdmin (BaseAdmin):
    list_display = ('name','description','edit')
    list_display_links = ('edit',)
    search_fields = ['name']
    list_per_page = 15
    #change_list_template = "admin/upload_area.html"
    form=Type_justificationForm
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'


admin.site.register(Type_justification, Type_justificationAdmin)
admin.site.register(Type_marking,Type_markingAdmin)
admin.site.register(Parameter,ParameterAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(Position, PositionAdmin)