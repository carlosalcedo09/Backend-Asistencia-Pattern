from apps.maintenance.models import Regions, Area, Company
from rest_framework import serializers

        
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields= '__all__'
        
