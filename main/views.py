from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from utenti.models import Profile


def nega_accesso_senza_profilo(request):
    """
    Funzione utilizzata dalle view per negare l'accesso agli utenti oauth loggati e sprovvisti di un profilo
    (perchè non hanno completato la registrazione del proprio profilo).

    :param request: request utente.
    :return: render della pagina scelta_profilo_oauth.
    """

    # if request.user.is_authenticated:
    #     try:
    #         Profile.objects.get(user=request.user.id)
    #     except Exception:
    #         return True

    if request.user.is_authenticated:
        profilo = Profile.objects.get(user=request.user.id)
        if len(profilo.indirizzo) == 0:
            return True
    return False


def index(request):
    """
    Mostra la pagina principale del sito, lista annunci.

    :param request: request utente.
    :return: redirect alla view lista_annunci.
    """

    return HttpResponseRedirect(reverse('annunci:lista_annunci'))


def handler404(request):
    """
    Custom handler per errore 404.

    :param request: request utente.
    :return: redirect alla pagina errore 404.
    """

    if request.user.is_authenticated():
        context = ({'base_template': 'main/base.html'})
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})
    else:
        context = ({'base_template': 'main/base_visitor.html'})
    return render(request, '404.html', status=404, context=context)


def handler500(request):
    """
        Custom handler per errore 500.

        :param request: request utente.
        :return: redirect alla pagina errore 500.
        """

    if request.user.is_authenticated():
        context = ({'base_template': 'main/base.html'})
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})
    else:
        context = ({'base_template': 'main/base_visitor.html'})
    return render(request, '500.html', status=500, context=context)
