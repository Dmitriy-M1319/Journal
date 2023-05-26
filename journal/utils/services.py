"""
Модуль вспомогательных сервисов
"""
from django.core.serializers.json import json

def load_post_data(request) -> dict:
    """
    Загрузить тело запроса из самого HTTP-запроса
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    return body_data

