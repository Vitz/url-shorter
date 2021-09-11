from django.contrib import admin

from .models import ShortUrl, AdminSettings


admin.register(ShortUrl)
admin.register(AdminSettings)
