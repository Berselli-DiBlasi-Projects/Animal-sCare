from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from utenti.models import Profile
from annunci.models import Annuncio, Servizio

class IsSameAnagraficaUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsSameUserOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari dei dati loggati.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id


class IsAnnuncioPossessorOrReadOnly(permissions.BasePermission):
    """
    update e delete concessi solo ai proprietari degli annunci.
    """
    def has_object_permission(self, request, view, obj):
        # print(obj.annuncio.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.annuncio.user == request.user


class IsRecensionePossessorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_recensore == request.user



class IsFlagAnnuncioCorrect(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        annuncio = Annuncio.objects.get(id=obj.annuncio.pk)
        return annuncio.user == request.user

class IsUserLogged(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsCompatibleUser(permissions.BasePermission):
    '''
    qui controllo se chi sta accettando un annuncio può farlo veramente

    un petsitter può pubblicare un annuncio di essere disponibile ad accudire un animale in un determinato
    periodo, e quindi un utente potrebbe decidere di accettare un annuncio

    invece un utente normale può andare a creare un'annuncio in cui riporta la necessità che gli venga accudito
    il proprio animale e questo annuncio può essere accettato solamente da un petsitter.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # id_utente = obj.user
        print(request.user)
        utente = Profile.objects.get(user=request.user)
        # print("utente permission ", utente)
        annuncio_petsitter = obj.annuncio_petsitter

        if annuncio_petsitter == True and utente.pet_sitter == False:
            #se l'annuncio osservato è di un petsitter e chi lo sta accettando è un utente normale
            # è okay
            return True

        if annuncio_petsitter == False and utente.pet_sitter == True:
            #se l'annuncio osservato è di un utente normale e chi lo sta accettando è un utente petsitter
            # è okay
            return True
        #per tutte le altre opzioni restituisco false
        return False