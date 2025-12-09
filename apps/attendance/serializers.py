from rest_framework import serializers
from .models import AttendanceMarking

class AttendanceMarkingSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(source='attendance.date')
    tipo = serializers.CharField(source='type_marking.name')
    hora = serializers.TimeField(source='hour', allow_null=True)
    observacion = serializers.CharField(source='observation')
    estado = serializers.CharField(source='state')

    class Meta:
        model = AttendanceMarking
        fields = ['fecha','tipo', 'hora', 'observacion', 'estado']
