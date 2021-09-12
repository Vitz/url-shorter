from django.shortcuts import render, redirect
from rest_framework import status, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import ShortUrl
from .serializers import ShortUrlSerializer, CreateUrlSerializer, UrlVisitors


class UrlView(ModelViewSet):
    queryset = ShortUrl.objects.all()

    def get_serializer_class(self):
        serializers = {
            'create': CreateUrlSerializer,
            'update': CreateUrlSerializer,
            'list': ShortUrlSerializer,
            'retrieve': ShortUrlSerializer,
            'partial_update': CreateUrlSerializer,
        }
        return serializers.get(self.action)

    def retrieve(self, request, pk=None):
        data = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer_class()(data, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data.get('url')
            instance, created = ShortUrl.objects.update_or_create(url=url)
            if created:
                instance.adder_ip = get_client_ip(request)
                instance.user_agent = get_user_agent(request)
                instance.save()
            return Response(ShortUrlSerializer(instance, context={'request': request}).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShortUrlView(APIView):
    def get(self, request, code, format=None):
        short_url = ShortUrl.objects.filter(code=code)[0]
        short_url.visitors = short_url.visitors + 1
        short_url.save()
        return redirect(short_url.url)


class VisitorsView(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = UrlVisitors
    queryset = ShortUrl.objects.all().order_by('-visitors')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    try:
        return request.META['HTTP_USER_AGENT']
    except:
        return ""