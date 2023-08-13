"""
Модуль встпомогательных сериализаторов данных
"""
from rest_framework import serializers


class MessageResponseSerializer(serializers.Serializer):
    """
    Сериализатор для отправки сообщений в HTTP-ответе
    """
    detail = serializers.CharField(max_length=255)
