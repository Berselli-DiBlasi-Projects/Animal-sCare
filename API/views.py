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
                             )
from annunci.views import recupera_annunci
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

class userInfoLogin(generics.RetrieveUpdateAPIView):
    """
    Questa view restituisce la lista completa degli utenti registrati
    """
    permission_classes = [IsSameUserOrReadOnly,IsUserLogged]
    serializer_class = DatiUtenteCompleti
    def get_object(self):
        """
        Modifico il query set in modo da ottenere l'utente con l'id
        prelevato dall'url
        """
        oid = self.kwargs['pk']
        return Profile.objects.get(user=oid)




# class anagraficaUtente(generics.RetrieveUpdateAPIView):
#     """
#      Questa view restituisce l'utente avente ID passato tramite URL
#      e ne permette la modifica
#     """
#     serializer_class = AnagraficaSerializer
#     permission_classes = [IsSameAnagraficaUserOrReadOnly]
#     # lookup_field = "pk"
#     def get_object(self):
#         oid = self.kwargs['pk']
#         return get_object_or_404(Profile, user=oid)
#
#     # def get_queryset(self):
#     #     """
#     #     Modifico il query set in modo da ottenere l'utente con l'id
#     #     prelevato dall'url
#     #     """
#     #     oid = self.kwargs['pk']
#     #     print("Anagrafica utente : ", oid)
#     #     obj = Profile.objects.filter(user=oid)
#     #     print(obj)
#     #     return obj

#
# class modificaUserInfoLogin(generics.RetrieveUpdateAPIView):
#     '''
#     endpoint per modificare i dati login utente
#     '''
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         oid = self.kwargs['pk']
#         return User.objects.filter(id=oid)
#
# class modificaAnagraficaUtente(generics.RetrieveUpdateAPIView):
#     '''
#     endpoint per modificare i dati dell'anagrafica dell'utente
#     '''
#     serializer_class = AnagraficaSerializer
#     # lookup_field = "pk"
#     def get_object(self):
#         oid = self.kwargs['pk']
#         return get_object_or_404(Profile, user=oid)


class listaAnnunci(generics.ListAPIView):
    """
     Questa view restituisce la lista completa di tutti gli annunci
     """
    # queryset = Annuncio.objects.all()
    serializer_class = AnnuncioConServizi

    def get_queryset(self):
        # data_odierna = datetime.now();
        # return Annuncio.objects.filter(user_accetta=None)
        return Servizio.objects.filter(annuncio__user_accetta__isnull=True)


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



# class servizi_richiesti(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Questa view restituisce i flag connessi ad un annuncio
#     e ne permette la modifica solamente se chi la richiama è il proprietario dell'annuncio
#     """
#     permission_classes = [IsFlagAnnuncioCorrect]
#     serializer_class = ServizioOffertoSerializer
#     def get_object(self):
#         """
#         Questa view restituisce i flag dell'annuncio avente ID passato tramite URL
#         """
#         oid = self.kwargs['pk']
#         return get_object_or_404(Servizio, annuncio=oid)


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


# class inserisciAnnuncio(APIView):
#         """
#         Mostra un elenco degli articoli presenti nel database e ne crea di nuovi!
#         """
#         permission_classes = [IsUserLogged]
#         def post(self, request):
#             serializer = AnnuncioSerializer(data=request.data)
#             if serializer.is_valid():
#                 # serializer.save()
#                 userprofile = Profile.objects.filter(user=self.request.user).first()
#                 print("userprofile",userprofile)
#                 if userprofile.pet_sitter:
#                     print("sono un petsitter")
#                     serializer.save(annuncio_petsitter=True, user=self.request.user)
#                 else:
#                     print("sono un utente normale")
#                     serializer.save(annuncio_petsitter=False, user=self.request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class inserisciAnnuncio(generics.CreateAPIView):
#     '''crea un nuovo annuncio'''
#     serializer_class = AnnuncioSerializer
#     # queryset = Annuncio.objects.all()
#     permission_classes = [IsUserLogged]
#     # devo controllare che tipo di utente sto maneggiando e fare quindi l'apposito metodo create o post
#
#     def perform_create(self, serializer):
#         ''' vado ad impostare automaticamente il flag annuncio_petsitter ed anche l'id del richiedente '''
#         userprofile = Profile.objects.filter(user=self.request.user).first()
#         print("userprofile",userprofile)
#         if userprofile.pet_sitter:
#             print("sono un petsitter")
#             serializer.save(annuncio_petsitter=True, user=self.request.user)
#         else:
#             print("sono un utente normale")
#             serializer.save(annuncio_petsitter=False, user=self.request.user)
#         # serializer.save()


class inserisciAnnuncio(generics.CreateAPIView):
    '''crea un nuovo annuncio'''
    serializer_class = AnnuncioConServizi
    # queryset = Annuncio.objects.all()
    permission_classes = [IsUserLogged]
    # devo controllare che tipo di utente sto maneggiando e fare quindi l'apposito metodo create o post

    # def perform_create(self, serializer):
    #     ''' vado ad impostare automaticamente il flag annuncio_petsitter ed anche l'id del richiedente '''
    #     userprofile = Profile.objects.filter(user=self.request.user).first()
    #     print("userprofile",userprofile)
    #     if userprofile.pet_sitter:
    #         print("sono un petsitter")
    #         serializer.save()
    #     else:
    #         print("sono un utente normale")
    #         serializer.save(user=self.request.user)
    #     # serializer.save()



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

class cercaUtente(generics.RetrieveAPIView):
    permission_classes = [IsUserLogged]
    serializer_class = DatiUtenteCompleti
    def get_object(self):
        name = self.kwargs['name']
        print(name)
        username_cercato = User.objects.get(username=name)
        profilo = Profile.objects.get(user=username_cercato)
        profilo.user.password=""
        return profilo

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




#
# class profiloUtenteAPI(APIView):
#     parser_classes = (FileUploadParser,)
#
#     '''
#     in questa classe vado a prendere in dettaglio un determinato utente
#     la modifica ed eliminazione può essere fatta solamente se colui che richiama la API
#     è il proprietario dell'account
#     '''
#
#     # def get_object(self, oid):
#     #     user = get_object_or_404(User, id=oid)
#     #     profilo = get_object_or_404(Profile, user=oid)
#     #     return user, profilo
#
#     def get(self, request, oid):
#         utente = User.objects.get(id=oid)
#         profilo = Profile.objects.get(user=oid)
#         utente_serializer = UserSerializer(utente)
#         profilo_serializer = ProfileSerializer(profilo)
#         return Response({
#             'utente': utente_serializer.data,
#             'profilo': profilo_serializer.data
#         })
#
#     def post(self, request, oid, filename, format=None):
#         print("request.data : ",request.data)
#         print("oid : ", oid)
#         print("request.data['utente'] : ", request.data['utente'])
#         print("request.data['profilo'] : ", request.data['profilo'])
#         print("request.user", request.user.username)
#         print("request.data['utente'].get('username')", request.data['utente'].get("username"))
#
#         if(request.user.username != request.data['utente'].get("username")):
#             raise PermissionDenied(_("Non puoi modificare dati che non ti appartengono"))
#
#
#         foto_profilo = request.FILES['foto_profilo']
#         if request.data['profilo'].get("pet_sitter") == False:
#             foto_pet = request.FILES['foto_pet']
#
#         user_serializer = UserSerializer(data=request.data['utente'])
#         profile_serializer = ProfileSerializer(data=request.data['profilo'])
#         # serializer = AnnuncioSerializer(data=request.data)
#
#         try:
#             user_serializer.is_valid(raise_exception=True)
#             profile_serializer.is_valid(raise_exception=True)
#         except serializers.ValidationError:
#             return Response({'utente': user_serializer.errors,
#                             'profilo': profile_serializer.errors
#                             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'utente': user_serializer.data,
#                              'profilo': profile_serializer.data
#                             }, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, oid):
#         print("request.data : ", request.data)
#
#         print("request.user", request.user.id)
#
#         if (request.user.id != oid):
#             raise PermissionDenied(_("Non puoi cancellare dati che non ti appartengono"))
#
#         utente = User.objects.get(id=oid)
#         profilo = Profile.objects.get(user=oid)
#         utente.delete()
#         profilo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
