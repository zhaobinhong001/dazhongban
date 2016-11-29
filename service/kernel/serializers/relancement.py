from __future__ import unicode_literals

from rest_framework import serializers
from ..models.relancement import Relancement

class RelancementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relancement
        fields = '__all__'