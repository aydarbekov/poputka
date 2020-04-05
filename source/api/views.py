from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.serializers import AnnouncementSerializer
from webapp.models import Announcements


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(photo=self.request.data.get('photo'))