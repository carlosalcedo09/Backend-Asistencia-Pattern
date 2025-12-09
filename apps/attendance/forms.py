from django import forms
from .models import Attendance, AttendanceMarking, Justification

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee','date','overtime','hours_worked','state']

class AttendanceMarkingForm (forms.ModelForm):
    class Meta:
        model = AttendanceMarking
        fields = ['type_marking','hour','observation','state']

class JustificationForm (forms.ModelForm):
    class Meta:
        model = Justification
        fields = ['type','reason','justification','state']