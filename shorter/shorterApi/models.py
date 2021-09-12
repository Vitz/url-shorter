

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShortUrl(models.Model):
    url = models.URLField(max_length=500, unique=True)
    short_url = models.URLField(max_length=100, blank=True, unique=True)
    adder_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    visitors = models.PositiveBigIntegerField(default=0)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)


class AdminSettings(models.Model):
    last_modify = models.DateTimeField(auto_now=True)
    default_url_length = models.IntegerField(default=8)
    host = models.URLField(max_length=500, default="http://127.0.0.1:8000")
    string = models.CharField(max_length=20, default="short")


@receiver(post_save, sender=ShortUrl)
def create_shorted(instance, created, **kwargs):
    last_settings = AdminSettings.objects.last()
    default_len = last_settings.default_url_length
    if created:
        import uuid
        code = uuid.uuid4().hex[:default_len].upper()
        instance.short_url = "{}/{}/{}".format(last_settings.host.rstrip('/'), last_settings.string , code)
        instance.code = code
        instance.save()




