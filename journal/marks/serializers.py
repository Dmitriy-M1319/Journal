from rest_framework import serializers
from .models import JournalCeil


class CeilSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalCeil
        fields = ('id', 'student', 'subject_class', 'mark', 'attendance')
