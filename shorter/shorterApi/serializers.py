from rest_framework import serializers

from .models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name ='ShortUrl-detail')
    class Meta:
        model = ShortUrl
        fields = ['id', 'url', 'short_url', 'adder_ip', 'user_agent', 'visitors', 'code']

    def create(self, validated_data):
        return ShortUrl(**validated_data)


class CreateUrlSerializer(serializers.Serializer):
    url = serializers.URLField()
    class Meta:
        fields = ['url']
    def create(self, validated_data):
        return ShortUrl(**validated_data)


class UrlVisitors(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = ['short_url', 'visitors']




