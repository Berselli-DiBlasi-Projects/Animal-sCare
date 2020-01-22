from django.urls import reverse, resolve
from main.views import index
import unittest


class TestUrls(unittest.TestCase):

    def test_index_url(self):
        path = reverse('main:index')
        self.assertEquals(resolve(path).func, index)
