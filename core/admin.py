from django.contrib import admin
from django.contrib.auth.models import  Group
# Default User va Group'ni admindan olib tashlash
admin.site.unregister(Group)
