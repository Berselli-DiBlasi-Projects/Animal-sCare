from django.urls import reverse, resolve
from annunci.views import lista_annunci, inserisci_annuncio, dettagli_annuncio, modifica_annuncio, elimina_annuncio
from annunci.views import elimina_annuncio_conferma, accetta_annuncio, conferma_annuncio, calendario, annunci_di_utente
import unittest


class TestUrls(unittest.TestCase):

    def test_lista_annunci_url(self):
        path = reverse('annunci:lista-annunci')
        self.assertEquals(resolve(path).func, lista_annunci)

    def test_inserisci_annuncio_url(self):
        path = reverse('annunci:inserisci_annuncio')
        self.assertEquals(resolve(path).func, inserisci_annuncio)

    def test_dettagli_annuncio_url(self):
        path = reverse('annunci:dettagli_annuncio', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, dettagli_annuncio)

    def test_modifica_annuncio_url(self):
        path = reverse('annunci:modifica_annuncio', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, modifica_annuncio)

    def test_elimina_annuncio_url(self):
        path = reverse('annunci:elimina_annuncio', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, elimina_annuncio)

    def test_elimina_annuncio_conferma_url(self):
        path = reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, elimina_annuncio_conferma)

    def test_accetta_annuncio_url(self):
        path = reverse('annunci:accetta_annuncio', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, accetta_annuncio)

    def test_conferma_annuncio_url(self):
        path = reverse('annunci:conferma_annuncio', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, conferma_annuncio)

    def test_calendario_url(self):
        path = reverse('annunci:calendario')
        self.assertEquals(resolve(path).func, calendario)

    def test_annunci_di_utente_url(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'user'})
        self.assertEquals(resolve(path).func, annunci_di_utente)
