from __future__ import unicode_literals

from rest_framework import serializers
from ..models.consumption import Consumption

class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumption
        fields = '__all__'