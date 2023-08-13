from rest_framework import viewsets
from rest_framework import permissions

from marks.models import JournalCeil
from marks.serializers import JournalCeilSerializer


class JournalCeilViewSet(viewsets.ModelViewSet):
    queryset = JournalCeil.objects.all()
    serializer_class = JournalCeilSerializer
    permission_classes = (permissions.IsAuthenticated,)

