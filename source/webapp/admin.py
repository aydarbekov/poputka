from django.contrib import admin

from accounts.models import Profiles
from webapp.models import Announcements

admin.site.register(Profiles)
admin.site.register(Announcements)

