from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from utenti.models import Profile
from annunci.models import Annuncio, Servizio

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

        annuncio_normale = Annuncio.objects.create(
            user=self.user_normale,
            annuncio_petsitter=False,
            titolo='Titolo annuncio',
            sottotitolo='Sottotitolo annuncio',
            descrizione='Descrizione annuncio',
            pet_coins=10,
            pet='Cane'
        )

        Servizio.objects.create(
            annuncio=annuncio_normale,
            passeggiate=True,
            cibo=True
        )

        annuncio_petsitter = Annuncio.objects.create(
            user=self.user_petsitter,
            annuncio_petsitter=True,
            titolo='Titolo annuncio',
            sottotitolo='Sottotitolo annuncio',
            descrizione='Descrizione annuncio',
            pet_coins=10,
            pet='Cane'
        )

        Servizio.objects.create(
            annuncio=annuncio_petsitter,
            passeggiate=True,
            cibo=True
        )

        self.user_oauth_login = Client()
        self.user_oauth = User.objects.create_user(username='oauth', password='12345')
        self.user_oauth_login.login(username='oauth', password='12345')

    def test_accetta_annuncio_normale_to_normale(self):
        response = self.user_normale_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_accetta_annuncio_petsitter_to_normale(self):
        response = self.user_petsitter_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_accetta_annuncio_unauthenticated_to_normale(self):
        response = self.user_unauthenticated.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_accetta_annuncio_normale_to_petsitter(self):
        response = self.user_normale_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_accetta_annuncio_petsitter_to_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_accetta_annuncio_unauthenticated_to_petsitter(self):
        response = self.user_unauthenticated.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_accetta_annuncio_normale_errato(self):
        response = self.user_normale_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_accetta_annuncio_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_accetta_annuncio_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_annunci_di_utente_unauthenticated(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'normale'})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_annunci_di_utente_authenticated_normale(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'normale'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_annunci_di_utente_authenticated_petsitter(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'petsitter'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_annunci_di_utente_authenticated_normale_to_other(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'petsitter'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_annunci_di_utente_authenticated_petsitter_to_other(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'normale'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_annunci_di_utente_unauthenticated_errato(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'errato'})
        response = self.user_unauthenticated.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_annunci_di_utente_authenticated_normale_errato(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'errato'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_annunci_di_utente_authenticated_petsitter_errato(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_annunci_di_utente_authenticated_normale_to_other_errato(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'errato'})
        response = self.user_normale_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_annunci_di_utente_authenticated_petsitter_to_other_errato(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'errato'})
        response = self.user_petsitter_login.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_calendario_normale(self):
        response = self.user_normale_login.get(reverse('annunci:calendario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/calendario.html')

    def test_calendario_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:calendario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/calendario.html')

    def test_calendario_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('annunci:calendario'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_conferma_annuncio_normale(self):
        response = self.user_normale_login.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/conferma_annuncio.html')

    def test_conferma_annuncio_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/conferma_annuncio.html')

    def test_conferma_annuncio_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_conferma_annuncio_normale_errato(self):
        response = self.user_normale_login.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_conferma_annuncio_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_conferma_annuncio_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_dettagli_annuncio_normale_errato(self):
        response = self.user_normale_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_dettagli_annuncio_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_dettagli_annuncio_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_dettagli_annuncio_normale_to_normale(self):
        response = self.user_normale_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_dettagli_annuncio_petsitter_to_normale(self):
        response = self.user_petsitter_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_dettagli_annuncio_normale_to_petsitter(self):
        response = self.user_normale_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_dettagli_annuncio_petsitter_to_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_dettagli_annuncio_unauthenticated_to_normale(self):
        response = self.user_unauthenticated.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_dettagli_annuncio_unauthenticated_to_petsitter(self):
        response = self.user_unauthenticated.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/dettagli_annuncio.html')

    def test_elimina_annuncio_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_elimina_annuncio_normale_to_himself(self):
        response = self.user_normale_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/elimina_annuncio.html')

    def test_elimina_annuncio_petsitter_to_normale(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_normale_to_petsitter(self):
        response = self.user_normale_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_petsitter_to_himself(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/elimina_annuncio.html')

    def test_elimina_annuncio_unauthenticated_to_normale(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_elimina_annuncio_unauthenticated_to_petsitter(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_elimina_annuncio_conferma_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_conferma_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_elimina_annuncio_conferma_normale_to_himself(self):
        response = self.user_normale_login.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_elimina_annuncio_conferma_petsitter_to_normale(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_conferma_normale_to_petsitter(self):
        response = self.user_normale_login.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_elimina_annuncio_conferma_petsitter_to_himself(self):
        response = self.user_petsitter_login.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/' == response.url

    def test_elimina_annuncio_conferma_unauthenticated_to_normale(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_elimina_annuncio_conferma_unauthenticated_to_petsitter(self):
        response = self.user_unauthenticated.get(reverse('annunci:elimina_annuncio_conferma', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_inserisci_annuncio_authenticated_normale(self):
        response = self.user_normale_login.get(reverse('annunci:inserisci_annuncio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/inserisci_annuncio.html')

    def test_inserisci_annuncio_authenticated_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:inserisci_annuncio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/inserisci_annuncio.html')

    def test_inserisci_annuncio_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('annunci:inserisci_annuncio'))
        self.assertEqual(response.status_code, 302)
        assert 'utenti/login' in response.url

    def test_lista_annunci_authenticated_normale(self):
        response = self.user_normale_login.get(reverse('annunci:lista_annunci'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_lista_annunci_authenticated_petsitter(self):
        response = self.user_petsitter_login.get(reverse('annunci:lista_annunci'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_lista_annunci_unauthenticated(self):
        response = self.user_unauthenticated.get(reverse('annunci:lista_annunci'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/lista_annunci.html')

    def test_modifica_annuncio_petsitter_errato(self):
        response = self.user_petsitter_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_modifica_annuncio_unauthenticated_errato(self):
        response = self.user_unauthenticated.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 10}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_modifica_annuncio_normale_to_himself(self):
        response = self.user_normale_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/modifica_annuncio.html')

    def test_modifica_annuncio_petsitter_to_normale(self):
        response = self.user_petsitter_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_modifica_annuncio_normale_to_petsitter(self):
        response = self.user_normale_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_modifica_annuncio_petsitter_to_himself(self):
        response = self.user_petsitter_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'annunci/modifica_annuncio.html')

    def test_modifica_annuncio_unauthenticated_to_normale(self):
        response = self.user_unauthenticated.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_modifica_annuncio_unauthenticated_to_petsitter(self):
        response = self.user_unauthenticated.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 2}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/login/' in response.url

    def test_accetta_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:accetta_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_annunci_di_utente_oauth_no_profilo_to_normale(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'normale'})
        response = self.user_oauth_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_annunci_di_utente_oauth_no_profilo_to_petsitter(self):
        path = reverse('annunci:annunci_di_utente', kwargs={'username': 'petsitter'})
        response = self.user_oauth_login.get(path)
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_calendario_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:calendario'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_conferma_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:conferma_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_dettagli_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:dettagli_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_elimina_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:elimina_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_inserisci_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:inserisci_annuncio'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_lista_annunci_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:lista_annunci'))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url

    def test_modifica_annuncio_oauth_no_profilo(self):
        response = self.user_oauth_login.get(reverse('annunci:modifica_annuncio', kwargs={'oid': 1}))
        self.assertEqual(response.status_code, 302)
        assert '/utenti/scegli_profilo/' in response.url
