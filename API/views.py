from rest_framework.exceptions import *
from rest_framework import generics
from django.contrib.auth.models import User
from recensioni.models import Recensione
from API.serializers import (AnnuncioSerializer,
                             AnnuncioConServizi,
                             DatiUtenteCompleti,
                             CompletaRegPetsitterSerializer,
                             CompletaRegUtenteNormale,
                             RecensioniSerializer,
                             ContattaciSerializer,
                             PetCoinsSerializer,
                             AccettaAnnuncioSerializer,
                             )
from annunci.views import ordina_annunci as ordina_geograficamente
from .permissions import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied


class userInfoLogin(generics.RetrieveAPIView):
    """
    Questa view restituisce la lista completa degli utenti registrati
    """
    serializer_class = DatiUtenteCompleti

    def get_object(self):
        """
        Modifico il query set in modo da ottenere l'utente con l'id
        prelevato dall'url
        """
        oid = self.kwargs['pk']
        return Profile.objects.get(user=oid)


class selfUserInfoLogin(generics.RetrieveUpdateDestroyAPIView):
    '''
    restituisco di default il profilo dell'utente loggato
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = DatiUtenteCompleti

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def perform_destroy(self, instance):
        profilo_da_eliminare = User.objects.get(id=instance.user.id)
        profilo_da_eliminare.is_active = False
        profilo_da_eliminare.save()
        logout(self.request)


class completaRegPetsitter(generics.RetrieveUpdateAPIView):
    '''
    completa l'inserimento dei dati per la registrazione di un petsitter
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegPetsitterSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class completaRegUtentenormale(generics.RetrieveUpdateAPIView):
    '''
    completa l'inserimento dei dati per un utente normale
    '''
    permission_classes = [IsSameUserOrReadOnly, IsUserLogged]
    serializer_class = CompletaRegUtenteNormale

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class listaAnnunci(generics.ListAPIView):
    """
     Questa view restituisce la lista completa di tutti gli annunci
    """
    serializer_class = AnnuncioSerializer

    def get_queryset(self):
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

        if tipo_utente == 'normale' and animale != '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, pet=animale, annuncio_petsitter=False)

        if tipo_utente == 'petsitter' and animale == '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, annuncio_petsitter=True)

        if tipo_utente == 'normale' and animale == '*':
            lista = Annuncio.objects.filter(user_accetta__isnull=True, annuncio_petsitter=False)

        if ordinamento == 'crescente' or ordinamento == 'decrescente':
            profilo_utente = Profile.objects.get(user=self.request.user)
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

    def perform_destroy(self, instance):
        annuncio_da_eliminare = Annuncio.objects.get(id=instance.annuncio.id)
        if annuncio_da_eliminare.user == self.request.user:
            annuncio_da_eliminare.delete()
        else:
            raise PermissionDenied()


class elencoAnnunciUtente(generics.ListAPIView):
    '''restituisce tutti gli annunci fatti da un utente'''
    serializer_class = AnnuncioConServizi

    def get_queryset(self):
        """
        Questa view restituisce l'annuncio avente ID passato tramite URL
        """
        oid = self.kwargs['pk']
        return Servizio.objects.filter(annuncio__user=oid, annuncio__user_accetta=None)


class inserisciAnnuncio(generics.CreateAPIView):
    '''crea un nuovo annuncio'''
    serializer_class = AnnuncioConServizi
    permission_classes = [IsUserLogged]


class accettaAnnuncio(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCompatibleUser, IsUserLogged]
    serializer_class = AccettaAnnuncioSerializer

    def get_object(self):
        """
        Questa view restituisce l'annuncio avente ID passato tramite URL
        """
        oid = self.kwargs['pk']
        return Annuncio.objects.get(id=oid)

    def perform_update(self, serializer):
        oid = self.kwargs['pk']
        annuncio_selezionato = Annuncio.objects.get(id=oid)
        utente_attivo = Profile.objects.get(user=self.request.user)
        # annuncio_selezionato.user_accetta = serializer.validated_data['user_accetta']
        if (utente_attivo.pet_sitter == True and annuncio_selezionato.annuncio_petsitter == False) or \
                (utente_attivo.pet_sitter == False and annuncio_selezionato.annuncio_petsitter == True):
            if serializer.validated_data['user_accetta'] == True:
                annuncio_selezionato.user_accetta = self.request.user
                annuncio_selezionato.save()
        else:
            content = 'non sei autorizzato ad accettare annunci della tua stessa categoria'
            raise PermissionDenied()


class calendarioUtente(generics.ListAPIView):
    permission_classes = [IsUserLogged]
    serializer_class = AnnuncioSerializer

    def get_queryset(self):
        user_request = self.request.user
        queryset = Annuncio.objects.filter(user_accetta=user_request)
        return queryset


class calendarioUtenteConFiltro(generics.ListAPIView):
    '''
        API per ordinamento degli annunci
        url : annunci/calendario/filtra/(?P<animale>[A-Za-z0-9*]+)/(?P<valido>^True+$|^False+$)

        Parametri :

        animale :       < Cane, Gatto, Coniglio, Volatile, Rettile, Altro >

        valido :   < True, False >

        Attenzione per ignorare il criterio di filtro per animale inserire " * "

        '''
    permission_classes = [IsUserLogged]
    serializer_class = AnnuncioSerializer

    def get_queryset(self):
        user_request = self.request.user
        queryset = Annuncio.objects.filter(user_accetta=user_request)
        animale = self.kwargs['animale']

        animali_ammessi = ["Cane", "Gatto", "Coniglio", "Volatile", "Rettile", "Altro"]

        if animale == '*':
            queryset = Annuncio.objects.filter(user_accetta=user_request)

        if animale in animali_ammessi:
            queryset = Annuncio.objects.filter(user_accetta=user_request,
                                               pet=animale)
        return queryset


class cercaUtente(generics.ListAPIView):
    serializer_class = DatiUtenteCompleti

    def get_queryset(self):
        name = self.kwargs['name']
        profili = []
        try:
            username_cercato = User.objects.get(username__exact=name)
            profilo = Profile.objects.get(user=username_cercato)
            profilo.user.password = ""
            profili.append(profilo)
            return profili
        except Exception:
            username_trovati = User.objects.filter(username__startswith=name)
            if len(username_trovati) == 0:
                username_trovati = User.objects.filter(username__contains=name)
            for user in username_trovati:
                p = Profile.objects.get(user=user)
                p.user.password = ""
                profili.append(p)
            return profili


class classificaUtenti(generics.ListAPIView):
    '''
    API per la classifica utente :

    tipo_utente : < petsitter > ,  < normale >, < * >

    criterio : < voti > , < recensioni >

    PER SELEZIONARE TUTTI GLI UTENTI INSERIRE ' * '

    NON È AMMESSO IGNORARE IL CRITERIO DI ORDINAMENTO

    '''
    serializer_class = DatiUtenteCompleti

    def get_queryset(self):
        criterio = self.kwargs['criterio']
        tipo_utente = self.kwargs['tipo_utente']

        # viene fatto sempre se si ignora il criterio di ricerca
        profili = Profile.objects.all()

        if tipo_utente == 'petsitter':
            profili = Profile.objects.filter(pet_sitter=True)

        if tipo_utente == 'normale':
            profili = Profile.objects.filter(pet_sitter=False)

        if criterio == 'voti':
            lista = list()
            for p in profili:
                voti = Recensione.objects.filter(user_recensito=p.user)
                somma = 0
                for v in voti:
                    somma += v.voto
                if len(voti) > 0:
                    media = somma / len(voti)
                else:
                    media = 0
                tupla = (p, media)
                lista.append(tupla)
            lista = sorted(lista, key=lambda tup: tup[1], reverse=True)
            profili = []
            for i in lista:
                profili.append(i[0])
            return profili

        if criterio == 'recensioni':
            lista = list()
            for p in profili:
                voti = Recensione.objects.filter(user_recensito=p.user)
                tupla = (p, len(voti))
                lista.append(tupla)
            lista = sorted(lista, key=lambda tup: tup[1], reverse=True)
            profili = []
            for i in lista:
                profili.append(i[0])
            return profili


class recensisciUtente(generics.CreateAPIView):
    serializer_class = RecensioniSerializer
    permission_classes = [IsUserLogged]

    def perform_create(self, serializer):
        nickname_recensore = self.request.user.username

        nickname_recensito = self.kwargs['utente']
        try:
            recensore = User.objects.get(username=nickname_recensore)
        except Exception:
            raise Exception("Utente recensore non trovato")
        try:
            recensito = User.objects.get(username=nickname_recensito)
        except Exception:
            raise Exception("Utente recensito non trovato")

        rec = Recensione.objects.filter(user_recensore=recensore, user_recensito=recensito)
        if len(rec) != 0:
            raise PermissionDenied("hai già recensito l'utente")

        if recensito != recensore:
            serializer.save(user_recensore=recensore, user_recensito=recensito)
        else:
            raise PermissionDenied("non puoi recensire te stesso")


class recensioniRicevute(generics.ListAPIView):
    serializer_class = RecensioniSerializer

    def get_queryset(self):
        # lista_recensioni = []
        nickname_cercato = self.kwargs['utente']
        try:
            recensito = User.objects.get(username=nickname_cercato)
        except Exception:
            raise Exception("Utente recensito non trovato")
        recensioni = Recensione.objects.filter(user_recensito=recensito)
        return list(recensioni)


class modificaPetCoins(generics.UpdateAPIView):
    serializer_class = PetCoinsSerializer
    permission_classes = [IsUserLogged]

    def get_object(self):
        profilo_selezionato = Profile.objects.get(user=self.request.user)
        return profilo_selezionato

    def perform_update(self, serializer):
        profilo_selezionato = Profile.objects.get(user=self.request.user)
        num = int(serializer.validated_data['pet_coins'])
        valori_ammessi = [50, 100, 200, -50, -100, -200]

        if num not in valori_ammessi:
            raise PermissionDenied("Valore non ammesso")

        profilo_selezionato.pet_coins += num
        profilo_selezionato.save()


class contattaciInPrivato(generics.CreateAPIView):
    serializer_class = ContattaciSerializer
    permission_classes = [IsUserLogged]

    def perform_create(self, serializer):
        email = EmailMessage(serializer.validated_data['titolo'],
                             'Messaggio dall\'utente: ' + self.request.user.username + "\n" +
                             serializer.validated_data['messaggio'], to=[settings.EMAIL_HOST_USER])
        email.send()
