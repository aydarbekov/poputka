from django.contrib import admin

from accounts.models import Profiles
from webapp.models import Announcements, ClientsInAnnounce, Car, CarModel, Review

admin.site.register(Profiles)
admin.site.register(Announcements)
admin.site.register(ClientsInAnnounce)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(Review)

