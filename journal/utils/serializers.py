"""
Модуль встпомогательных сериализаторов данных
"""
from rest_framework import serializers


class MessageResponseSerializer(serializers.Serializer):
    """
    Сериализатор для отправки сообщений в HTTP-ответе
    """
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=255)
