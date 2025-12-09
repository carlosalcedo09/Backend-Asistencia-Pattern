from django import forms
from .models import Schedule, Schedule_Detail


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['description','check_in_time','check_out_time','tolerance','break_time','working_days']

class ScheduleDetailForm(forms.ModelForm):
    class Meta:
        model = Schedule_Detail
        fields = ['employee','schedule','start_date','end_date']

