from __future__ import unicode_literals

from rest_framework import serializers

from ..models.certufucate import Certufucate

class CertufucateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certufucate
        fields = '__all__'
