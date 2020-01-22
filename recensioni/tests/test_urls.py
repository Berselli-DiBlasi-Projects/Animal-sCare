from django.urls import reverse, resolve
from recensioni.views import nuova_recensione, recensioni_ricevute
import unittest


class TestUrls(unittest.TestCase):

    def test_nuova_recensione_url(self):
        path = reverse('recensioni:nuova_recensione', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, nuova_recensione)

    def test_recensioni_ricevute_url(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'user'})
        self.assertEquals(resolve(path).func, recensioni_ricevute)
