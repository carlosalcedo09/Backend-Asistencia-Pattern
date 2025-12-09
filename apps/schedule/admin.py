from django.contrib import admin
from apps.schedule.models import Schedule, Schedule_Detail
from apps.schedule.forms import ScheduleForm,ScheduleDetailForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from apps.subadmin import RootSubAdmin


class ScheduleDetailAdmin(RootSubAdmin):
    list_display = ('employee','schedule','start_date','end_date','edit')
    list_display_links = ('edit',)
    search_fields = ['employee','schedule']
    list_filter =['schedule']
    list_per_page = 15
    form=ScheduleDetailForm

    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

class ScheduleAdmin (RootSubAdmin):
    list_display = ('description','check_in_time','check_out_time','tolerance','break_time','working_days','edit')
    list_display_links = ('edit',)
    search_fields = ['description']
    list_per_page = 15
    #change_list_template = "admin/upload_area.html"
    form=ScheduleForm
    
    def edit(self, obj):
        return format_html("<img src={icon_url}>", icon_url=settings.ICON_EDIT_URL)
    
    edit.short_description = '->'

admin.site.register(Schedule_Detail, ScheduleDetailAdmin)
admin.site.register(Schedule, ScheduleAdmin)