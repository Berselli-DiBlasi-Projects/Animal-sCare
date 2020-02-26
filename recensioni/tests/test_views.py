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
        self.profilo.indirizzo='Via Vivarelli'
        self.profilo.citta='Modena'
        self.profilo.provincia='Modena'
        self.profilo.regione='Emilia Romagna'
        self.profilo.latitudine=0
        self.profilo.longitudine=0
        self.profilo.telefono=3391234567
        self.profilo.pet_coins=100
        self.profilo.foto_profilo=None
        self.profilo.pet_sitter=False
        self.profilo.nome_pet='Ugo'
        self.profilo.pet='Cane'
        self.profilo.razza='Shihtzu'
        self.profilo.eta=12
        self.profilo.caratteristiche='Allergico a quasi tutto'
        self.profilo.save()

        self.user_normale_login.login(username='normale', password='12345')

        self.user_petsitter_login = Client()
        self.user_petsitter = User.objects.create_user(username='petsitter', password='12345')
        self.profilo = Profile.objects.get(user=self.user_petsitter)
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

    def test_nuova_recensione_normale(self):
        response = self.user_normale_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/nuova_recensione.html')

    def test_nuova_recensione_petsitter(self):
        response = self.user_petsitter_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/nuova_recensione.html')

    def test_nuova_recensione_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_nuova_recensione_normale_errato(self):
        response = self.user_normale_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_nuova_recensione_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_nuova_recensione_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_recensioni_ricevute_authenticated_normale(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'normale'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/recensioni_ricevute.html')

    def test_recensioni_ricevute_authenticated_petsitter(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'petsitter'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/recensioni_ricevute.html')

    def test_recensioni_ricevute_authenticated_normale_to_other(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'petsitter'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/recensioni_ricevute.html')

    def test_recensioni_ricevute_authenticated_petsitter_to_other(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'normale'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensioni/recensioni_ricevute.html')

    def test_recensioni_ricevute_authenticated_normale_errato(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_recensioni_ricevute_authenticated_petsitter_errato(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_recensioni_ricevute_unauthenticated_errato(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_nuova_recensione_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_recensioni_ricevute_oauth_no_profilo_to_normale(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'normale'})
        response = self.user_oauth_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_recensioni_ricevute_oauth_no_profilo_to_petsitter(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'petsitter'})
        response = self.user_oauth_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url
