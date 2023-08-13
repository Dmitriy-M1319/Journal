from rest_framework import serializers
from .models import JournalCeil


class JournalCeilSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalCeil
        fields = ('__all__')
