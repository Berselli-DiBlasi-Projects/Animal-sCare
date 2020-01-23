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
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_nuova_recensione_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('recensioni:nuova_recensione', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

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
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_recensioni_ricevute_authenticated_petsitter_errato(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_recensioni_ricevute_unauthenticated_errato(self):
        path = reverse('recensioni:recensioni_ricevute', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url
