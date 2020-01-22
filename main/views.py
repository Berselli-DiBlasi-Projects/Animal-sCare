from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    """
    Mostra la pagina principale del sito, lista annunci.

    :param request: request utente.
    :return: redirect alla view lista-annunci.
    """

    return HttpResponseRedirect(reverse('annunci:lista-annunci'))
