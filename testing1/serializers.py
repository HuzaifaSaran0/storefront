from rest_framework import serializers
from .models import Car



class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'color', 'unit_price', 'description']
    
    # products_count = serializers.IntegerField(read_only=True) 