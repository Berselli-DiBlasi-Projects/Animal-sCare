from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import TestCase
from annunci.models import Annuncio, Servizio
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='12345')
        self.annuncio = Annuncio.objects.create(
            user=self.user,
            annuncio_petsitter=False,
            titolo='Titolo annuncio',
            sottotitolo='Sottotitolo annuncio',
            descrizione='Descrizione annuncio',
            pet_coins=10,
            pet='Cane'
        )

        Servizio.objects.create(
            annuncio=self.annuncio,
            passeggiate=True,
            cibo=True
        )

    def test_foto_annuncio_or_default(self):
        self.assertEquals(self.annuncio.logo_annuncio_or_default(), static("/images/annuncio_default.jpg"))
