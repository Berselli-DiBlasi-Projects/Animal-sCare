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

        self.profilo = Profile.objects.get(user=self.user_normale)
        # profilo.user = self.user_normale,
        self.profilo.indirizzo = 'Via Vivarelli'
        self.profilo.citta = 'Modena'
        self.profilo.provincia = 'Modena'
        self.profilo.regione = 'Emilia Romagna'
        self.profilo.latitudine = 0
        self.profilo.longitudine = 0
        self.profilo.telefono = 3391234567
        self.profilo.pet_coins = 100
        self.profilo.foto_profilo = None
        self.profilo. pet_sitter = False
        self.profilo.nome_pet = 'Ugo'
        self.profilo.pet = 'Cane'
        self.profilo.razza = 'Shihtzu'
        self.profilo.eta = 12
        self.profilo.caratteristiche = 'Allergico a quasi tutto'
        self.profilo.save()

        self.user_normale_login.login(username='normale', password='12345')

        self.user_petsitter_login = Client()
        self.user_petsitter = User.objects.create_user(username='petsitter', password='12345')
        self.profilo = Profile.objects.get(user=self.user_petsitter)

        # profilo.user=self.user_petsitter,
        self.profilo.indirizzo='Via Vivarelli'
        self.profilo.citta='Modena'
        self.profilo.provincia='Modena'
        self.profilo.regione='Emilia Romagna'
        self.profilo.latitudine=0
        self.profilo.longitudine=0
        self.profilo.telefono=3391234567
        self.profilo.pet_coins=100
        self.profilo.foto_profilo=None
        self.profilo.pet_sitter=True
        self.profilo.nome_pet='Tobi'
        self.profilo.pet='Cane'
        self.profilo.razza='Meticcio'
        self.profilo.eta=3
        self.profilo.caratteristiche='Allergico alle noci'
        self.profilo.foto_pet=None
        self.profilo.descrizione='Socievole'
        self.profilo.hobby='Cinema, Musica, Sport'
        self.profilo.save()

        self.user_petsitter_login.login(username='petsitter', password='12345')

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

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
        path = reverse('utenti:edit_profile', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/modifica_profilo.html')

    def test_edit_profile_authenticated_normale_errato(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 2})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_edit_profile_authenticated_petsitter_errato(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_edit_profile_authenticated_petsitter_corretto(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/modifica_profilo.html')

    def test_edit_profile_unauthenticated(self):
        path = reverse('utenti:edit_profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_logout_user_unauthenticated(self):
        path = reverse('utenti:utenti_logout')
        response = self.user_unauthenticated.get(path)
        assert 'utenti/login' in response.url

    def test_logout_user_authenticated_normale(self):
        path = reverse('utenti:utenti_logout')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_logout_user_authenticated_petsitter(self):
        path = reverse('utenti:utenti_logout')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_cerca_utenti_unauthenticated_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_unauthenticated.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)

    def test_cerca_utenti_authenticated_petsitter_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_petsitter_login.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cerca_utenti.html')

    def test_cerca_utenti_authenticated_normale_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_normale_login.get(path, {'cerca': 'user'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cerca_utenti.html')

    def test_cerca_utenti_unauthenticated_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_unauthenticated.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cerca_utenti.html')

    def test_cerca_utenti_authenticated_petsitter_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_petsitter_login.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cerca_utenti.html')

    def test_cerca_utenti_authenticated_normale_senza_nome(self):
        path = reverse('utenti:cerca_utenti')
        response = self.user_normale_login.get(path, {'cerca': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/cerca_utenti.html')

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
        self.assertTemplateUsed(response, 'utenti/classifica.html')

    def test_classifica_authenticated_normale(self):
        path = reverse('utenti:classifica')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/classifica.html')

    def test_classifica_authenticated_petsitter(self):
        path = reverse('utenti:classifica')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/classifica.html')

    def test_elimina_profilo_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/elimina_profilo.html')

    def test_elimina_profilo_authenticated_petsitter(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/elimina_profilo.html')

    def test_elimina_profilo_authenticated_petsitter_errato(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_profilo_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_elimina_profilo_conferma_authenticated_normale(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_elimina_profilo_conferma_authenticated_petsitter(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_elimina_profilo_conferma_authenticated_petsitter_errato(self):
        path = reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_profilo_conferma_unauthenticated(self):
        path = reverse('utenti:elimina_profilo', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_login_user_unauthenticated(self):
        path = reverse('utenti:utenti_login')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/login.html')

    def test_login_user_authenticated_normale(self):
        path = reverse('utenti:utenti_login')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_login_user_authenticated_petsitter(self):
        path = reverse('utenti:utenti_login')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_oauth_normale_unauthenticated(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_normale/' in response.url

    def test_oauth_normale_authenticated_normale(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_oauth_normale_authenticated_petsitter(self):
        path = reverse('utenti:oauth_normale')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_oauth_petsitter_unauthenticated(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/oauth_petsitter/' in response.url

    def test_oauth_petsitter_authenticated_normale(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_oauth_petsitter_authenticated_petsitter(self):
        path = reverse('utenti:oauth_petsitter')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_unauthenticated(self):
        path = reverse('utenti:registrazione')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/registrazione.html')

    def test_registrazione_authenticated_normale(self):
        path = reverse('utenti:registrazione')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_authenticated_petsitter(self):
        path = reverse('utenti:registrazione')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_normale_unauthenticated(self):
        path = reverse('utenti:registrazione_normale')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/registrazione_normale.html')

    def test_registrazione_normale_authenticated_normale(self):
        path = reverse('utenti:registrazione_normale')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_normale_authenticated_petsitter(self):
        path = reverse('utenti:registrazione_normale')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_petsitter_unauthenticated(self):
        path = reverse('utenti:registrazione_petsitter')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/registrazione_petsitter.html')

    def test_registrazione_petsitter_authenticated_normale(self):
        path = reverse('utenti:registrazione_petsitter')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_registrazione_petsitter_authenticated_petsitter(self):
        path = reverse('utenti:registrazione_petsitter')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_scelta_profilo_oauth_unauthenticated(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_scelta_profilo_oauth_authenticated_normale(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_scelta_profilo_oauth_authenticated_petsitter(self):
        path = reverse('utenti:scelta_profilo_oauth')
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_view_profile_authenticated_normale_to_normale(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 1})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_normale.html')

    def test_view_profile_unauthenticated_to_normale(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 1})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_normale.html')

    def test_view_profile_authenticated_petsitter_to_normale(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 1})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_normale.html')

    def test_view_profile_authenticated_normale_to_petsitter(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 2})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_petsitter.html')

    def test_view_profile_unauthenticated_to_petsitter(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 2})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_petsitter.html')

    def test_view_profile_authenticated_petsitter_to_petsitter(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 2})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/profilo_petsitter.html')

    def test_view_profile_authenticated_normale_errato(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 10})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_view_profile_unauthenticated_errato(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 10})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_view_profile_authenticated_petsitter_errato(self):
        path = reverse('utenti:view_profile', kwargs={'oid': 10})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_cassa_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:cassa'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_cerca_utenti_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:cerca_utenti'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_check_username_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:check_username'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_classifica_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:classifica'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_edit_profile_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:edit_profile', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_elimina_profilo_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:elimina_profilo', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_elimina_profilo_conferma_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:elimina_profilo_conferma', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_login_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:utenti_login'))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_logout_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:utenti_logout'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_oauth_petsitter_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:oauth_petsitter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/oauth_profilo_petsitter.html')

    def test_oauth_normale_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:oauth_normale'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/oauth_profilo_normale.html')

    def test_registrazione_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:registrazione'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_registrazione_normale_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:registrazione_normale'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_registrazione_petsitter_user_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:registrazione_petsitter'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_scelta_profilo_oauth_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:scelta_profilo_oauth'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'utenti/scelta_utente_oauth.html')

    def test_view_profilo_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('utenti:view_profile', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url
