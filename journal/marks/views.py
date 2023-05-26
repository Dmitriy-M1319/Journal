from rest_framework import viewsets
from marks.models import JournalCeil
from marks.serializers import CeilSerializer


class CeilViewSet(viewsets.ModelViewSet):
    queryset = JournalCeil.objects.all()
    serializer_class = CeilSerializer
