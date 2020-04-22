from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Profiles
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profiles
    exclude = []


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)


