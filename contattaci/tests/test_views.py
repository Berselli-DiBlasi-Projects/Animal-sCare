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
            pet_sitter=False,
            nome_pet='Ugo',
            pet='Cane',
            razza='Shihtzu',
            eta=12,
            caratteristiche='Allergico a quasi tutto'
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

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

    def test_contattaci_normale(self):
        response = self.user_normale_login.get(reverse('contattaci:contattaci'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contattaci.html')

    def test_contattaci_petsitter(self):
        response = self.user_petsitter_login.get(reverse('contattaci:contattaci'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contattaci.html')

    def test_contattaci_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('contattaci:contattaci'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_contattaci_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('contattaci:contattaci'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url
