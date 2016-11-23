from __future__ import unicode_literals

from rest_framework import serializers
from ..models.transfer import Transfer


class TransferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
