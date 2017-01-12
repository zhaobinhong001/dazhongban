from __future__ import unicode_literals

from rest_framework import serializers
from service.kernel.models.consumption import Contract

class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ('sender', 'receiver')