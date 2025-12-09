from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    time_in_company = forms.CharField(label="Tiempo en la Empresa", required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Employee
        fields = ['document_type','document_number','full_name','profile_picture','email','cellphone','gender','has_children','area','position',
                'is_active','date_entry','type_pension','code_afp','user']
    
        widgets = {
        }
        

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk: 
           self.fields['time_in_company'].initial = self.instance.get_time_in_company()


