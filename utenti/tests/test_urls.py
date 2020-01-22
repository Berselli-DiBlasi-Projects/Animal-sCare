from django.urls import reverse, resolve
from utenti.views import login_user, registrazione, registrazione_normale, registrazione_petsitter, check_username
from utenti.views import logout_user, view_profile, edit_profile, cassa, classifica, cerca_utenti, elimina_profilo
from utenti.views import scelta_profilo_oauth, oauth_normale, oauth_petsitter, elimina_profilo_conferma
import unittest


class TestUrls(unittest.TestCase):

    def test_login_url(self):
        path = reverse('utenti:utenti-login')
        self.assertEquals(resolve(path).func, login_user)

    def test_registrazione_url(self):
        path = reverse('utenti:registrazione')
        self.assertEquals(resolve(path).func, registrazione)

    def test_registrazione_normale_url(self):
        path = reverse('utenti:registrazione-normale')
        self.assertEquals(resolve(path).func, registrazione_normale)

    def test_registrazione_petsitter_url(self):
        path = reverse('utenti:registrazione-petsitter')
        self.assertEquals(resolve(path).func, registrazione_petsitter)

    def test_logout_url(self):
        path = reverse('utenti:utenti-logout')
        self.assertEquals(resolve(path).func, logout_user)

    def test_view_profile_url(self):
        path = reverse('utenti:view-profile', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, view_profile)

    def test_edit_profile_url(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, edit_profile)

    def test_cassa_url(self):
        path = reverse('utenti:cassa')
        self.assertEquals(resolve(path).func, cassa)

    def test_classifica_url(self):
        path = reverse('utenti:classifica')
        self.assertEquals(resolve(path).func, classifica)

    def test_cerca_utenti_url(self):
        path = reverse('utenti:cerca_utenti')
        self.assertEquals(resolve(path).func, cerca_utenti)

    def test_elimina_profilo_url(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, elimina_profilo)

    def test_elimina_profilo_conferma_url(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        self.assertEquals(resolve(path).func, elimina_profilo_conferma)

    def test_check_username_url(self):
        path = reverse('utenti:check_username')
        self.assertEquals(resolve(path).func, check_username)

    def test_scelta_profilo_oauth_url(self):
        path = reverse('utenti:scelta_profilo_oauth')
        self.assertEquals(resolve(path).func, scelta_profilo_oauth)

    def test_oauth_normale_url(self):
        path = reverse('utenti:oauth_normale')
        self.assertEquals(resolve(path).func, oauth_normale)

    def test_oauth_petsitter_url(self):
        path = reverse('utenti:oauth_petsitter')
        self.assertEquals(resolve(path).func, oauth_petsitter)
