from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from utenti.models import Profile
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import ContattaciForm
from django.core.mail import EmailMessage
from django.conf import settings
from main.views import nega_accesso_senza_profilo


@login_required(login_url='/utenti/login/')
def contattaci(request):
    """
    Permette all'utente di contattare gli amministratori del sito scrivendo un titolo e un messaggio.
    Il messaggio viene recapitato alla mailbox del sito, con mittente la mailbox del sito stessa.
    Nel corpo della mail viene inserito lo username dell'utente così che i messaggi non siano anonimi.

    :param request: request utente.
    :return: render pagina contattaci.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    form = ContattaciForm(request.POST or None)

    context = {
        "form": form,
        "base_template": 'main/base.html'
    }

    if form.is_valid():
        # manda email
        email = EmailMessage(form.cleaned_data['titolo'],
                             'Messaggio dall\'utente: ' + request.user.username + "\n" +
                             form.cleaned_data['messaggio'], to=[settings.EMAIL_HOST_USER])
        email.send()
        return render(request, 'success.html', context)

    context.update({'user_profile': Profile.objects.filter(user=request.user).first()})

    return render(request, 'contattaci.html', context)
