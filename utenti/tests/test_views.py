from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from utenti.models import Profile
import pytest


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.user_unauthenticated = Client()
        self.user_normale_login = Client()
        self.user_normale = User.objects.create_user(username='normale', password='12345')
        Profile.objects.create(
            user=self.user_normale,
            indirizzo='Via Vivarelli',
            citta='Modena',
            provincia='Modena',
            regione='Emilia Romagna',
            latitudine=0,
            longitudine=0,
            telefono=3391234567,
            pet_coins=100,
            foto_profilo=None,
            pet_sitter=False
        )
        self.user_normale_login.login(username='normale', password='12345')

        self.user_petsitter_login = Client()
        self.user_petsitter = User.objects.create_user(username='petsitter', password='12345')
        Profile.objects.create(
            user=self.user_petsitter,
            indirizzo='Via Vivarelli',
            citta='Modena',
            provincia='Modena',
            regione='Emilia Romagna',
            latitudine=0,
            longitudine=0,
            telefono=3391234567,
            pet_coins=100,
            foto_profilo=None,
            pet_sitter=True,
            nome_pet='Tobi',
            pet='Cane',
            razza='Meticcio',
            eta=3,
            caratteristiche='Allergico alle noci',
            foto_pet=None,
            descrizione='Socievole',
            hobby='Cinema, Musica, Sport'
        )
        self.user_petsitter_login.login(username='petsitter', password='12345')

    def test_cassa_authenticated_normale(self):
        response = self.user_normale_login.get(reverse('utenti:cassa'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cassa.html')

    def test_cassa_authenticated_petsitter(self):
        response = self.user_petsitter_login.get(reverse('utenti:cassa'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cassa.html')

    def test_cassa_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('utenti:cassa'))
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_edit_profile_authenticated_normale(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_authenticated_normale_errato(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 2})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_authenticated_petsitter_errato(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_authenticated_petsitter_corretto(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_unauthenticated(self):
        path = reverse('utenti:edit-profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_logout_user_unauthenticated(self):
        path = reverse('utenti:utenti-logout')
        response = self.user_unauthenticated.get(path)
        assert 'utenti/login' in response.url

    def test_logout_user_authenticated_normale(self):
        path = reverse('utenti:utenti-logout')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_logout_user_authenticated_petsitter(self):
        path = reverse('utenti:utenti-logout')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_cerca_utenti_unauthenticated_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_unauthenticated.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_authenticated_petsitter_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_petsitter_login.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_authenticated_normale_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_normale_login.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_unauthenticated_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_unauthenticated.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_authenticated_petsitter_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_petsitter_login.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_authenticated_normale_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_normale_login.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)

    def test_check_username_presente_unauthenticated(self):
        path = reverse('utenti:check_username')
        response = self.user_unauthenticated.get(path, {'username': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_check_username_presente_authenticated_normale(self):
        path = reverse('utenti:check_username')
        response = self.user_normale_login.get(path, {'username': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_check_username_presente_authenticated_petsitter(self):
        path = reverse('utenti:check_username')
        response = self.user_petsitter_login.get(path, {'username': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_classifica_unauthenticated(self):
        path = reverse('utenti:classifica')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_classifica_authenticated_normale(self):
        path = reverse('utenti:classifica')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_classifica_authenticated_petsitter(self):
        path = reverse('utenti:classifica')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_elimina_profilo_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_elimina_profilo_authenticated_petsitter(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_elimina_profilo_authenticated_petsitter_errato(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_elimina_profilo_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_elimina_profilo_conferma_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_elimina_profilo_conferma_authenticated_petsitter(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_elimina_profilo_conferma_authenticated_petsitter_errato(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_elimina_profilo_conferma_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_login_user_unauthenticated(self):
        path = reverse('utenti:utenti-login')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_login_user_authenticated_normale(self):
        path = reverse('utenti:utenti-login')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_login_user_authenticated_petsitter(self):
        path = reverse('utenti:utenti-login')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_oauth_normale_unauthenticated(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_normale/' in response.url

    def test_oauth_normale_authenticated_normale(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_oauth_normale_authenticated_petsitter(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_oauth_petsitter_unauthenticated(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_petsitter/' in response.url

    def test_oauth_petsitter_authenticated_normale(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_oauth_petsitter_authenticated_petsitter(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_unauthenticated(self):
        path = reverse('utenti:registrazione')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_registrazione_authenticated_normale(self):
        path = reverse('utenti:registrazione')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_authenticated_petsitter(self):
        path = reverse('utenti:registrazione')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_normale_unauthenticated(self):
        path = reverse('utenti:registrazione-normale')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_registrazione_normale_authenticated_normale(self):
        path = reverse('utenti:registrazione-normale')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_normale_authenticated_petsitter(self):
        path = reverse('utenti:registrazione-normale')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_petsitter_unauthenticated(self):
        path = reverse('utenti:registrazione-petsitter')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_registrazione_petsitter_authenticated_normale(self):
        path = reverse('utenti:registrazione-petsitter')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_registrazione_petsitter_authenticated_petsitter(self):
        path = reverse('utenti:registrazione-petsitter')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_scelta_profilo_oauth_unauthenticated(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_scelta_profilo_oauth_authenticated_normale(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_scelta_profilo_oauth_authenticated_petsitter(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' in response.url

    def test_view_profile_authenticated_petsitter(self):
        path = reverse('utenti:view-profile', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_unauthenticated(self):
        path = reverse('utenti:view-profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_profile_authenticated_petsitter(self):
        path = reverse('utenti:view-profile', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
