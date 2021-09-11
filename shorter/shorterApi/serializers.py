from rest_framework import serializers

from .models import ShortUrl


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = ['url',]
        # fields = ['url', 'short_url', 'adder_ip', 'user_agent']


