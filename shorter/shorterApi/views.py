from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortUrl



class UrlView(APIView):

    def get(self, request, url, format=None):

        try:
            license = Url.objects.get()
        except:
            license = None


        return Response("responce")







