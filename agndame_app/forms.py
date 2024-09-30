from django import forms
from .models import Appointment

# Clase para validar formulario de la clase Appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name_client','lastname_client','email','date','hour','category','service','worker','note']
        labels = {
            'name_client': 'Nombre',
            'lastname_client': 'Apellidos',
            'email': 'Email',
            'date': 'Fecha',
            'hour': 'Hora',
            'category': 'Categoría',
            'service': 'Servicio',
            'worker': 'Empleado',
            'note': 'Nota',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour': forms.TimeInput(attrs={'type': 'time'}),
        }