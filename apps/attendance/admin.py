from django.contrib import admin
from apps.base.admin import BaseAdmin
from apps.attendance.models import Attendance, AttendanceMarking, Justification
from apps.subadmin import  SubAdmin,RootSubAdmin
from django.conf import settings
from django.utils.html import format_html
from apps.attendance.forms import AttendanceForm,AttendanceMarkingForm, JustificationForm
from apps.attendance.choices import StatusChoices,StatusMarkingChoices,StatusJustificationChoices
from unfold.decorators import display


class SummaryAttendanceMarkingAdmin (BaseAdmin):
    list_display = ('get_employee','type_marking','hour','observation','show_status_customized_color','edit')
    list_display_links = ('edit',)
    search_fields = ['attendance__employee']
    list_filter= ['type_marking', 'attendance__employee', 'attendance__date']
    list_per_page = 15
    readonly_fields = ('state',)
    form= AttendanceMarkingForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

    def get_employee(self, obj):
        return obj.attendance.employee  
    get_employee.short_description = 'Empleado'

    @display(
        description="Estado",
        ordering="state",
        label={
            StatusMarkingChoices.Lateness: "warning",
            StatusMarkingChoices.On_Time: "success",
            StatusMarkingChoices.Reces: "dark",
            StatusMarkingChoices.Before_time: "info",
        },
    )

    def show_status_customized_color(self, obj):
        return obj.state

class JustificationSubAdmin (SubAdmin):
    model = Justification
    list_display = ('type','reason','justification','show_status_customized_color','edit')
    list_display_links = ('edit',)
    list_per_page= 10
    form= JustificationForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

    @display(
        description="Estado",
        ordering="state",
        label={
            StatusJustificationChoices.Rejected: "warning",
            StatusJustificationChoices.Approved: "success",
            StatusJustificationChoices.Pending: "dark",
        },
    )

    def show_status_customized_color(self, obj):
        return obj.state

    

class AttendanceMarkingSubAdmin (SubAdmin):
    model = AttendanceMarking
    list_display = ('type_marking','hour','observation','show_status_customized_color','edit')
    list_display_links = ('edit',)
    list_per_page= 10
    readonly_fields = ('state',)
    form= AttendanceMarkingForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

    @display(
        description="Estado",
        ordering="state",
        label={
            StatusMarkingChoices.Lateness: "warning",
            StatusMarkingChoices.On_Time: "success",
            StatusMarkingChoices.Reces: "dark",
            StatusMarkingChoices.Before_time: "info",
        },
    )

    def show_status_customized_color(self, obj):
        return obj.state


class AttendanceAdmin (RootSubAdmin):
    list_display= ('date','employee','hours_worked','overtime','show_status_customized_color','edit')
    list_display_links = ('edit',)
    search_fields = ['employee']
    list_filter= ['employee','state']
    subadmins = [AttendanceMarkingSubAdmin,JustificationSubAdmin]
    form =  AttendanceForm 

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

    @display(
        description="Estado",
        ordering="state",
        label={
            StatusChoices.Pending: "warning",
            StatusChoices.Completed: "success",
            StatusChoices.In_progress: "dark",
            StatusChoices.Justified: "info",
        },
    )

    def show_status_customized_color(self, obj):
        return obj.state


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(AttendanceMarking, SummaryAttendanceMarkingAdmin)