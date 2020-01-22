from django.contrib.auth.decorators import login_required
from utenti.models import Profile
from django.shortcuts import render
from .forms import ContattaciForm
from django.core.mail import EmailMessage
from django.conf import settings


@login_required(login_url='/utenti/login/')
def contattaci(request):
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
