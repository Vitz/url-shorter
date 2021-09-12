from django.contrib import admin

from .models import ShortUrl, AdminSettings


class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ["url", 'short_url', 'visitors',  'adder_ip']
    fields = ['url', 'short_url', 'adder_ip', 'visitors', 'user_agent']
    readonly_fields = ['user_agent', 'adder_ip', 'visitors', 'short_url', 'user_agent']


class AdminSettingsAdmin(admin.ModelAdmin):
    ordering = ['-last_modify',]
    list_display = ["last_modify", 'default_url_length', 'host', 'string']
    fields = ['last_modify', 'default_url_length', 'host', 'string']
    readonly_fields = ['last_modify',]


admin.site.register(ShortUrl, ShortUrlAdmin)
admin.site.register(AdminSettings, AdminSettingsAdmin)
