from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from utenti.models import Profile
from annunci.models import Annuncio, Servizio
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory





import datetime


# Create your tests here.

class listAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_normale = User.objects.create_user(username='normale', password='12345')
        self.token_user_normale = Token.objects.create(user=self.user_normale)
        self.profilo_normale = Profile.objects.get(user=self.user_normale)
        self.profilo_normale.indirizzo = 'Via Vivarelli'
        self.profilo_normale.citta = 'Modena'
        self.profilo_normale.provincia = 'Modena'
        self.profilo_normale.regione = 'Emilia Romagna'
        self.profilo_normale.latitudine = 0
        self.profilo_normale.longitudine = 0
        self.profilo_normale.telefono = 1234567890
        self.profilo_normale.pet_coins = 100
        self.profilo_normale.foto_profilo = None
        self.profilo_normale.pet_sitter = False
        self.profilo_normale.nome_pet = 'Ugo'
        self.profilo_normale.pet = 'Cane'
        self.profilo_normale.razza = 'Shihtzu'
        self.profilo_normale.eta = 12
        self.profilo_normale.caratteristiche = 'Allergico a quasi tutto'
        self.profilo_normale.save()

        self.user_petsitter = User.objects.create_user(username='petsitter', password='12345')
        self.token_petsitter = Token.objects.create(user=self.user_petsitter)

        self.profilo_petsitter = Profile.objects.get(user=self.user_petsitter)
        self.profilo_petsitter.indirizzo = 'Via Vivarelli'
        self.profilo_petsitter.citta = 'Modena'
        self.profilo_petsitter.provincia = 'Modena'
        self.profilo_petsitter.regione = 'Emilia Romagna'
        self.profilo_petsitter.latitudine = 0
        self.profilo_petsitter.longitudine = 0
        self.profilo_petsitter.telefono = 3391234567
        self.profilo_petsitter.pet_coins = 100
        self.profilo_petsitter.foto_profilo = None
        self.profilo_petsitter.pet_sitter = True
        # self.profilo_petsitter.nome_pet = 'Tobi'
        # self.profilo_petsitter.pet = 'Cane'
        # self.profilo_petsitter.razza = 'Meticcio'
        # self.profilo_petsitter.eta = 3
        # self.profilo_petsitter.caratteristiche = 'Allergico alle noci'
        # self.profilo_petsitter.foto_pet = None
        self.profilo_petsitter.descrizione = 'Socievole'
        self.profilo_petsitter.hobby = 'Cinema, Musica, Sport'
        self.profilo_petsitter.save()

        self.user_petsitter_no_profilo = User.objects.create_user(
            username='petsitter_no_profilo', password='12345')
        self.token_user_petsitter_no_profilo = Token.objects.create(user=self.user_petsitter_no_profilo)


        self.user_normale_no_profilo = User.objects.create_user(
            username='normale_no_profilo', password='12345')
        self.token_user_normale_no_profilo = Token.objects.create(user=self.user_normale_no_profilo)


        self.user_da_cancellare = User.objects.create_user(
            username='user_da_cancellare', password='12345')
        self.token_user_da_cancellare = Token.objects.create(user=self.user_da_cancellare)


        # DEFINISCO GLI ANNUNCI:

        self.annuncio_normale = Annuncio.objects.create(
            user=self.user_normale,
            annuncio_petsitter=False,
            titolo='Titolo annuncio Nomale',
            sottotitolo='Sottotitolo annuncio',
            descrizione='Descrizione annuncio',
            pet_coins=10,
            pet='Cane'
        )

        Servizio.objects.create(
            annuncio=self.annuncio_normale,
            passeggiate=True,
            cibo=True
        )

        self.annuncio_petsitter = Annuncio.objects.create(
            user=self.user_petsitter,
            annuncio_petsitter=True,
            titolo='Titolo annuncio PETSITTER',
            sottotitolo='Sottotitolo annuncio',
            descrizione='Descrizione annuncio',
            pet_coins=10,
            pet='Cane'
        )

        Servizio.objects.create(
            annuncio=self.annuncio_petsitter,
            passeggiate=True,
            cibo=True
        )


    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = "http://127.0.0.1:8000/api/rest-auth/registration/"
        data = {
            "username": "resttest1",
            "email": "test1@rest.com",
            "password1": "cambiami12",
            "password2": "cambiami12",
            "first_name": "rest_first_name",
            "last_name": "rest_last_name"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_account(self):
        """
        Ensure we can login into an existing account
        """

        url = "http://127.0.0.1:8000/api/rest-auth/login/"
        data = {
            "username": "normale",
            "password": "12345"
        }
        response = self.client.post(url, data, format='json')
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_completa_registrazione_normale(self):

        data = {
                "user": {
                    "username": "completa",
                    "first_name": "profilo",
                    "last_name": "normale",
                },
                "indirizzo": "via rossi",
                "citta": "fermo",
                "provincia": "FM",
                "regione": "Marche",
                "telefono": "1234567890",
                "foto_profilo": None,
                "nome_pet": "aaa",
                "pet": "Cane",
                "razza": "meticcio",
                "eta": 1,
                "caratteristiche": "morbidissimo",
                "foto_pet": None
            }
        url = reverse("API:API-registra-utente-normale")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale_no_profilo.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_completa_registrazione_petsitter(self):

        data = {
                "user": {
                    "username": "completa",
                    "first_name": "profilo",
                    "last_name": "normale",
                },
                "indirizzo": "via rossi",
                "citta": "fermo",
                "provincia": "FM",
                "regione": "Marche",
                "telefono": "1234567890",
                "foto_profilo": None,
                "descrizione" : 'Socievole',
                "hobby" : 'Cinema, Musica, Sport',
            }
        url = reverse("API:API-registra-petsitter")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_petsitter_no_profilo.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_self_profilo_loggato(self):

        url = reverse("API:API-self-user-info")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_petsitter_no_profilo.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_self_profilo_loggato(self):

        token_h = "Token " + str(Token.objects.get(user=self.user_petsitter))
        headers = {"Authorization": token_h}
        url = reverse("API:API-self-user-info")
        response = self.client.delete(url,  headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_self_profilo_non_loggato(self):
        url = reverse("API:API-self-user-info")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_profilo_loggato(self):
        url = reverse("API:API-self-user-info")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_da_cancellare.key)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_lista_annunci(self):
        url = reverse("API:API-lista-annunci")
        response = self.client.get(url, format='json')
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lista_annunci_filtrata_parametri_generici(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        url = reverse("API:API-ordina-annunci-animale-distanza-utente",
                      kwargs={'animale': '*',
                              'ordinamento': '*',
                              'tipo_utente': '*'
                              }
                      )
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lista_annunci_filtrata_con_criterio(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        url = reverse("API:API-ordina-annunci-animale-distanza-utente",
                      kwargs={'animale': 'Cane',
                              'ordinamento': 'crescente',
                              'tipo_utente': 'normale'
                              }
                      )
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_dettaglio_annuncio(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        url = reverse("API:API-dettaglio-annuncio",
                      kwargs={'pk': 1}
                      )
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_annuncio_utente_non_loggato(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        url = reverse("API:API-dettaglio-annuncio",
                      kwargs={'pk': 1}
                      )
        print(url)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_annuncio_utente_loggato(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        da_cancellare = Annuncio.objects.get(user=self.user_normale)
        url = reverse("API:API-dettaglio-annuncio",
                      kwargs={'pk': da_cancellare.pk}
                      )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_annunci_di_un_utente(self):
        # url = "http://127.0.0.1:8000/api/annunci/ordina/*/*/*/"
        url = reverse("API:API-elenco-annunci-utente",
                      kwargs={'pk': 1}
                      )
        print(url)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modifica_annuncio_utente(self):
        url = reverse("API:API-dettaglio-annuncio",
                      kwargs={'pk': self.annuncio_petsitter.pk}
                      )
        data = {
            "annuncio": {
                "data_inizio": "2021-04-08T17:30:00",
                "data_fine": "2022-04-08T17:30:00",
                "annuncio_petsitter": 'false',
                "titolo": "titolo annuncio modificato",
                "sottotitolo": "sottotitolo annuncio",
                "descrizione": "descrizione modificata",
                "pet_coins": 1,
                "pet": "Cane",
                "logo_annuncio": None,
                # "user_accetta": None
            },
            "passeggiate": 'true',
            "pulizia_gabbia": 'true',
            "ore_compagnia": 'true',
            "cibo": 'true',
            "accompagna_dal_vet": 'true'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_inserisci_nuovo_annuncio(self):

        data = {
            "annuncio": {
                "data_inizio": "2021-04-08T17:30:00",
                "data_fine": "2022-04-08T17:30:00",
                "annuncio_petsitter": 'false',
                "titolo": "titolo annuncio",
                "sottotitolo": "sottotitolo annuncio",
                "descrizione": "descrizione",
                "pet_coins": 1,
                "pet": "Cane",
                "logo_annuncio": None,
                # "user_accetta": None
            },
            "passeggiate": 'true',
            "pulizia_gabbia": 'false',
            "ore_compagnia": 'true',
            "cibo": 'false',
            "accompagna_dal_vet": 'false'
        }

        url = reverse("API:API-nuovo-annuncio")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_accetta_annuncio_petsitter_da_petsitter(self):
        data = {
            "user_accetta": "true"
        }

        url = reverse("API:API-accetta-annuncio", kwargs={'pk': self.annuncio_petsitter.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_accetta_annuncio_normale_da_normale(self):
        data = {
            "user_accetta": "true"
        }

        url = reverse("API:API-accetta-annuncio", kwargs={'pk': self.annuncio_normale.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_accetta_annuncio_normale_da_petsitter(self):

        data = {
            "user_accetta": "true"
            }

        url = reverse("API:API-accetta-annuncio", kwargs={'pk':self.annuncio_normale.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accetta_annuncio_petsitter_da_normale(self):

        data = {
            "user_accetta": "true"
            }
        url = reverse("API:API-accetta-annuncio", kwargs={'pk':self.annuncio_petsitter.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_calendario_utente_loggato(self):
        url = reverse("API:API-calendario-utente")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calendario_utente_non_loggato(self):
        url = reverse("API:API-calendario-utente")
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_calendario_utente_loggato_filtrato(self):
        url = reverse("API:API-calendario-utente-con-filtro-annunci",
                      kwargs={'animale': 'Cane'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calendario_utente_non_loggato_filtrato(self):
        url = reverse("API:API-calendario-utente-con-filtro-annunci",
                      kwargs={'animale': 'Cane'})
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cerca_utente_username_esatto(self):
        url = reverse("API:API-cerca-utente",
                      kwargs={'name': self.user_normale.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cerca_utente_username_parziale(self):
        url = reverse("API:API-cerca-utente",
                      kwargs={'name': 'nor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_modifica_pet_coins_user_normale(self):
        data = {
            "pet_coins": '50'
            }
        url = reverse("API:API-petcoins-utenti")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modifica_pet_coins_errati_user_normale(self):
        data = {
            "pet_coins": '6443'
            }
        url = reverse("API:API-petcoins-utenti")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modifica_pet_coins_petsitter(self):
        data = {
            "pet_coins": '50'
            }
        url = reverse("API:API-petcoins-utenti")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modifica_pet_coins_errati_petsitter(self):
        data = {
            "pet_coins": '6443'
            }
        url = reverse("API:API-petcoins-utenti")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_modifica_pet_coins_user_non_loggato(self):
        data = {
            "pet_coins": '50'
            }
        url = reverse("API:API-petcoins-utenti")
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_recensisci_utente(self):
        data = {
                "titolo": "Recensione",
                "descrizione": "prova",
                "voto": 3,
            }
        #  nell'url viene specificato l'username dell'utente che si vuole recensire
        url = reverse("API:API-recensisci-utenti",
                      kwargs={
                          'utente': self.user_petsitter.username
                      }
                      )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.post(url, data=data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recensisci_te_stesso(self):
        data = {
            "titolo": "Recensione",
            "descrizione": "prova",
            "voto": 3,
        }
        #  nell'url viene specificato l'username dell'utente che si vuole recensire
        url = reverse("API:API-recensisci-utenti",
                      kwargs={
                          'utente': self.user_petsitter.username
                      }
                      )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_petsitter.key)
        response = self.client.post(url, data=data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modifica_recensione(self):
        data = {
            "titolo": "Recensione",
            "descrizione": "prova",
            "voto": 3,
        }
        #  nell'url viene specificato l'username dell'utente che si vuole recensire
        url = reverse("API:API-recensisci-utenti",
                      kwargs={
                          'utente': self.user_petsitter.username
                      }
                      )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_normale.key)
        response = self.client.post(url, data=data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)