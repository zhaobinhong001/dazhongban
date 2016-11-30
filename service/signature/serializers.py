from rest_framework import serializers

from .models import Signature


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        exclude = ('owner',)
