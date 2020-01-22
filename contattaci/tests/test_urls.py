from django.urls import reverse, resolve
from contattaci.views import contattaci
import unittest


class TestUrls(unittest.TestCase):

    def test_contattaci_url(self):
        path = reverse('contattaci:contattaci')
        self.assertEquals(resolve(path).func, contattaci)
