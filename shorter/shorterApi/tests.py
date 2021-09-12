from http import HTTPStatus
from django.test import TestCase
from .models import *

class GenerateUrl(TestCase):
    def test_generated_code_in_shorted_url(self):
        a_s = AdminSettings()
        a_s.save()
        s_u = ShortUrl(url = "https://www.google.com")
        s_u.save()
        self.assertIn(s_u.code, s_u.short_url)

    def test_code_len_in_shorted_url(self):
        default_url_length = 10
        a_s = AdminSettings(default_url_length=default_url_length)
        a_s.save()
        s_u = ShortUrl(url = "https://www.google.com")
        s_u.save()
        self.assertEqual(len(s_u.code), default_url_length)

    def test_redirection_works(self):
        a_s = AdminSettings()
        a_s.save()
        url = "https://www.google.com"
        s_u = ShortUrl(url=url)
        s_u.save()
        response = self.client.get(s_u.short_url)
        self.assertEqual(str(response.url).rstrip('/'), url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_short_url(self):
        AdminSettings().save()
        url = "https://www.o2.pl"
        response = self.client.post("/urls/", data={"url":url})
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.ACCEPTED])
        self.assertEqual(ShortUrl.objects.last().url, url)

    def test_retrieve_url(self):
        AdminSettings().save()
        url = "https://www.o2.pl"
        self.client.post("/urls/", data={"url":url})
        pk = ShortUrl.objects.last().pk
        response = self.client.get("/urls/{}/".format(pk))
        self.assertEqual(response.json()["url"], url)

