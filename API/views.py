from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from utenti.models import Profile
from annunci.models import Annuncio, Servizio
from API.serializers import (AnagraficaSerializer,
                                AnnuncioSerializer,
                                UserSerializer,
                                ServizioOffertoSerializer,
                                AnnuncioConServizi,
                                DatiUtenteCompleti,
                                CompletaRegPetsitterSerializer,
                                CompletaRegUtenteNormale,
                             )
from annunci.views import ordina_annunci as ordina_geograficamente
from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from .permissions import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


# class userInfoLogin(generics.RetrieveUpdateAPIView):
#     """
#     Questa view restituisce la lista completa degli utenti registrati
#     """
#     permission_classes = [IsSameUserOrReadOnly]
#     serializer_class = UserSerializer
#     def get_queryset(self):
#         """
#         Modifico il query set in modo da ottenere l'utente con l'id
#         prelevato dall'url
#         """
#         oid = self.kwargs['pk']
#         return User.objects.filter(id=oid)

class userInfoLogin(generics.RetrieveAPIView):
    """
    Questa view restituisce la lista completa degli utenti registrati
    """
    # permission_classes = [IsSameUserOrReadOnly,IsUserLogged]
    serializer_class = DatiUtenteCompleti
    def get_object(self):
        """
        Modifico il query set in modo da ottenere l'utente con l'id
        prelevato dall'url
        """
        oid = self.kwargs['pk']
        return Profile.objects.get(user=oid)

class selfUserInfoLogin(generics.RetrieveUpdateAPIView):
    '''
    restituisco di default il profilo dell'utente loggato
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = DatiUtenteCompleti

    def get_object(self):

        return Profile.objects.get(user=self.request.user)

class completaRegPetsitter(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegPetsitterSerializer
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class completaRegUtentenormale(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegUtenteNormale
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class listaAnnunci(generics.ListAPIView):
    """
     Questa view restituisce la lista completa di tutti gli annunci
     """
    # queryset = Annuncio.objects.all()
    serializer_class = AnnuncioSerializer

    def get_queryset(self):
        # data_odierna = datetime.now();
        # return Annuncio.objects.filter(user_accetta=None)
        return Annuncio.objects.filter(user_accetta__isnull=True)


class ordinaAnnunci(generics.ListAPIView):
    '''
    API per ordinamento degli annunci
    url : /api/annunci/ordina/ < animale > / < ordinamento > / < tipo_utente > /

    Parametri :

    animale :       < Cane, Gatto, Coniglio, Volatile, Rettile, Altro >

    ordinamento :   < crescente, decrescente>

    tipo_utente :   < petsitter, normale >

    Attenzione per ignorare il criterio di ordinamento inserire " * "

    in tal caso se inseriti tutti '*' fornirà i dati normalmente come lista annunci
    '''
    serializer_class = AnnuncioSerializer
    def get_queryset(self):
        ordinamento = self.kwargs['ordinamento']
        tipo_utente = self.kwargs['tipo_utente']
        animale = self.kwargs['animale']
        lista = Annuncio.objects.filter(user_accetta__isnull=True)

        if tipo_utente == '*' and animale != '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, pet=animale)

        if tipo_utente == '*' and animale == '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True)

        if tipo_utente == 'petsitter' and animale != '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, pet=animale, annuncio_petsitter=True)

        if tipo_utente == 'normale'and animale != '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, pet=animale, annuncio_petsitter=False)

        if tipo_utente == 'petsitter' and animale == '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, annuncio_petsitter=True)

        if tipo_utente == 'normale'and animale == '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, annuncio_petsitter=False)

        if ordinamento == 'crescente' or ordinamento == 'decrescente':
            profilo_utente = Profile.objects.get(user=self.request.user)
            indici = []
            indici = ordina_geograficamente(profilo_utente, lista, ordinamento)

            lista = list(lista)
            new_annunci_validi = list()
            # Ordina annunci_validi
            for i, annuncio in enumerate(lista):
                new_annunci_validi.append(lista[indici[i]])
            return new_annunci_validi

        return lista

class dettaglioAnnuncio(generics.RetrieveUpdateDestroyAPIView):
    """
    Questa view restituisce l'annuncio avente ID passato tramite URL
    e ne permette la modifica
    """
    permission_classes = [IsAnnuncioPossessorOrReadOnly]
    serializer_class = AnnuncioConServizi
    def get_object(self):
        """
        Questa view restituisce i flag dell'annuncio avente ID passato tramite URL
        """
        oid = self.kwargs['pk']
        return Servizio.objects.get(annuncio=oid)


class elencoAnnunciUtente(generics.ListAPIView):
    '''restituisce tutti gli annunci fatti da un utente'''
    serializer_class = AnnuncioConServizi
    permission_classes = [IsUserLogged]
    def get_queryset(self):
        """
        Questa view restituisce l'annuncio avente ID passato tramite URL
        """
        oid = self.kwargs['pk']
        return Servizio.objects.filter(annuncio__user=oid, annuncio__user_accetta = None)


class inserisciAnnuncio(generics.CreateAPIView):
    '''crea un nuovo annuncio'''
    serializer_class = AnnuncioConServizi
    # queryset = Annuncio.objects.all()
    permission_classes = [IsUserLogged]


class accettaAnnuncio(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCompatibleUser,IsUserLogged]
    serializer_class = AnnuncioConServizi
    def get_object(self):
        """
        Questa view restituisce l'annuncio avente ID passato tramite URL
        """
        oid = self.kwargs['pk']
        return Servizio.objects.get(annuncio=oid)
    #
    # def perform_update(self, serializer):
    #     user_accetta = self.request.user
    #     serializer.save(user_accetta=user_accetta)


class calendarioUtente(generics.ListAPIView):
    permission_classes = [IsUserLogged]
    serializer_class = AnnuncioSerializer
    def get_queryset(self):
        user_request = self.request.user
        print("user", user_request)

        queryset = Annuncio.objects.filter(user_accetta=user_request)
        print("queryset ", queryset)

        return queryset


class cercaUtente(APIView):
    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try :
            username_cercato = User.objects.get(username__exact=name)
            profilo = Profile.objects.get(user=username_cercato)
            profilo.user.password=""
            serializers = DatiUtenteCompleti(profilo,many=False)
            return Response(serializers.data)
        except Exception:
            username_trovati = User.objects.filter(username__startswith=name)
            print("username trovati : ", username_trovati)
            profili = []
            for user in username_trovati:
                p = Profile.objects.get(user=user)
                p.user.password = ""
                profili.append(p)
            serializers = DatiUtenteCompleti(profili, many=True)
            return Response(serializers.data)





# #################################################
#                          DA CANCELLARE
# #################################################



class elencoservizi(APIView):
    '''
    in questa classe prendo la lista di tutti gli utenti registrati sul sito.
    solo per scopi di debug
    DA CANCELLARE
    '''

    def get(self, request):
        data = Servizio.objects.all()
        serializer = ServizioOffertoSerializer(data, many=True)
        return Response(serializer.data)

class ListaUtentiRegistrati(APIView):
    '''
    in questa classe prendo la lista di tutti gli utenti registrati sul sito.
    solo per scopi di debug
    DA CANCELLARE
    '''

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ListaAnagraficheRegistrate(APIView):
    '''
    in questa classe prendo la lista di tutti gli utenti registrati sul sito.
    solo per scopi di debug
    DA CANCELLARE
    '''

    def get(self, request):
        profili = Profile.objects.all()
        serializer = AnagraficaSerializer(profili, many=True)
        return Response(serializer.data)


