from rest_framework import serializers
from .models import SimTonKho, SimDaBan

class SimTonKhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimTonKho
        fields = '__all__'

class SimDaBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimDaBan
        fields = '__all__'
