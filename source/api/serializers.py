from rest_framework import serializers

from webapp.models import Announcements


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = ('id', 'author', 'type', 'description', 'place_from', 'place_to', 'departure_time', 'seats', 'luggage', 'price', 'photo', 'status', 'clients')
