from django.db import models

# Create your models here.

class ShortUrl(models.Model):
    url = models.URLField(max_length=500)
    short_url = models.URLField(max_length=100)
    adder_ip = models.IPAddressField(null=True)
    user_agent = models.TextField(null=True, blank=True)
    visitors = models.PositiveBigIntegerField(default=0)


class AdminSettings(models.Model):
    last_modify = models.DateTimeField(auto_now=True)
    default_url_length = models.IntegerField(default=8)


