from django.shortcuts import render
from .models import Annuncio, Servizio
from utenti.models import User, Profile
from recensioni.models import Recensione
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import AnnuncioForm, ServizioForm
from django.db.models import Avg
from datetime import datetime, timedelta, timezone
from django.core.mail import EmailMessage
from math import sin, cos, sqrt, atan2, radians

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/utenti/login/')
def accetta_annuncio(request, oid):
    """
    Effettua le operazioni di accettazione annuncio quando un utente clicca l'omonimo button in una view Dettagli
    annuncio. E' incluso anche l'invio di una notifica via mail al proprietario dell'annuncio.

    :param request: request utente.
    :param oid: l'id dell'annuncio accettato.
    :return: redirect alla home.
    """

    annuncio = Annuncio.objects.filter(id=oid).first()
    user_profile = Profile.objects.filter(user=request.user).first()
    inserzionista_profile = Profile.objects.filter(user=annuncio.user).first()

    if user_profile.pet_sitter != annuncio.annuncio_petsitter:
        if user_profile.pet_sitter:

            user_profile.pet_coins = user_profile.pet_coins + annuncio.pet_coins
            annuncio.user_accetta = request.user
            user_profile.save()
            annuncio.save()

            # manda email
            utente_inserzionista = User.objects.filter(pk=inserzionista_profile.user.pk).first()
            utente_accetta = User.objects.filter(pk=user_profile.user.pk).first()

            email = EmailMessage('Il tuo annuncio è stato accettato',
                                 'L\'utente ' + utente_accetta.username + ' ha accettato il tuo annuncio. Fai il '
                                                                          'login su Animal\'sCare per controllare '
                                                                          'subito!',
                                 to=[utente_inserzionista.email])
            email.send()
        else:
            if user_profile.pet_coins >= annuncio.pet_coins:
                user_profile.pet_coins = user_profile.pet_coins - annuncio.pet_coins
                inserzionista_profile.pet_coins = inserzionista_profile.pet_coins + annuncio.pet_coins
                annuncio.user_accetta = request.user
                user_profile.save()
                inserzionista_profile.save()
                annuncio.save()

                # manda email
                utente_inserzionista = User.objects.filter(pk=inserzionista_profile.user.pk).first()
                utente_accetta = User.objects.filter(pk=user_profile.user.pk).first()
                email = EmailMessage('Il tuo annuncio è stato accettato',
                                     'L\'utente ' + utente_accetta.username + ' ha accettato il tuo annuncio. Fai il '
                                                                              'login su Animal\'sCare per controllare '
                                                                              'subito!',
                                     to=[utente_inserzionista.email])
                email.send()
            else:
                return HttpResponseRedirect(reverse('main:index'))
    return HttpResponseRedirect(reverse('main:index'))


def annunci_di_utente(request, username):
    """
    Mostra l'elenco degli annunci di un singolo utente.

    :param request: request utente.
    :param username: username dell'utente di cui mostrare gli annunci.
    :return: render lista annunci.
    """

    utente_richiesto = User.objects.filter(username=username).first()

    dati = recupera_annunci(request)

    annunci_validi = dati.get('annunci_validi').filter(user=utente_richiesto, user_accetta__isnull=True)

    sel_pet = dati.get('sel_pet')
    sel_categoria = dati.get('sel_categoria')
    annunci = dati.get('annunci')
    annunci_recensioni = {}
    annunci_voti = {}

    for annuncio in annunci_validi:
        annunci[annuncio] = Profile.objects.filter(user=annuncio.user).first()
        annunci_recensioni[annuncio] = Recensione.objects.filter(user_recensito=annuncio.user).count()
        voti = Recensione.objects.all().filter(user_recensito=annuncio.user).aggregate(Avg('voto'))
        if voti.get('voto__avg') is None:
            voti['voto__avg'] = 0

        annunci_voti[annuncio] = voti.get('voto__avg')

    context = {
        'annunci': annunci,
        'sel_categoria': sel_categoria,
        'sel_pet': sel_pet,
        'annunci_voti': annunci_voti,
        'annunci_recensioni': annunci_recensioni,
        'username': username
    }

    if not request.user.is_authenticated():
        context.update({'base_template': 'main/base_visitor.html'})
        return render(request, 'annunci/lista_annunci.html', context)
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        context.update({'base_template': 'main/base.html'})
        context.update({'user_profile': user_profile})
        return render(request, 'annunci/lista_annunci.html', context)


@login_required(login_url='/utenti/login/')
def calendario(request):
    """
    Mostra il calendario contenente tutti gli impegni passati e futuri, aperti e chiusi (contornati in verde e in
    rosso rispettivamente nel template) dell'utente loggato e che ha fatto la richiesta.

    :param request: request utente.
    :return: render del calendario.
    """

    dati = recupera_annunci(request)

    annunci_autore = dati.get('annunci_validi').filter(user=request.user).exclude(user_accetta__isnull=True)
    annunci_accettati = dati.get('annunci_validi').filter(user_accetta=request.user)
    annunci_validi = annunci_autore | annunci_accettati

    sel_pet = dati.get('sel_pet')
    sel_categoria = dati.get('sel_categoria')
    annunci = dati.get('annunci')
    annunci_recensioni = {}
    annunci_voti = {}

    for annuncio in annunci_validi:
        annunci[annuncio] = Profile.objects.filter(user=annuncio.user).first()
        annunci_recensioni[annuncio] = Recensione.objects.filter(user_recensito=annuncio.user).count()
        voti = Recensione.objects.all().filter(user_recensito=annuncio.user).aggregate(Avg('voto'))
        if voti.get('voto__avg') is None:
            voti['voto__avg'] = 0

        annunci_voti[annuncio] = voti.get('voto__avg')

    user_profile = Profile.objects.filter(user=request.user).first()

    context = {
        'base_template': 'main/base.html',
        'user_profile': user_profile,
        'annunci': annunci,
        'sel_categoria': sel_categoria,
        'sel_pet': sel_pet,
        'annunci_voti': annunci_voti,
        'annunci_recensioni': annunci_recensioni
    }

    return render(request, 'annunci/calendario.html', context)


@login_required(login_url='/utenti/login/')
def conferma_annuncio(request, oid):
    """
    Mostra una pagina per chiedere la conferma dell'accettazione di un annuncio da parte di un utente connesso.

    :param request: request utente.
    :param oid: l'id dell'annuncio accettato.
    :return: render di conferma annuncio.
    """

    annuncio = Annuncio.objects.filter(id=oid).first()
    context = {'annuncio': annuncio, 'base_template': 'main/base.html',
               'user_profile': Profile.objects.filter(user=request.user).first()}

    return render(request, 'annunci/conferma_annuncio.html', context)


def controllo_pet_coins(userprofile, pet_coins):
    """
    Controllo del valore dei pet coins nel saldo profilo dell'utente.

    :param userprofile: profilo utente.
    :param pet_coins: il valore in pet coins da controllare.
    :return: True oppure un messaggio di errore.
    """

    if not userprofile.pet_sitter and userprofile.pet_coins < int(pet_coins):
        return 'Errore: verifica di avere un saldo in pet coins sufficiente per inserire l\'annuncio.'

    return True


def dettagli_annuncio(request, oid):
    """
    Mostra i dettagli di un singolo annuncio.

    :param request: request utente.
    :param oid: l'id dell'annuncio.
    :return: render della pagina dettagli_annuncio.
     """

    if request.user.is_authenticated():
        context = {'base_template': 'main/base.html'}
        context.update({'user': User.objects.get(username=request.user)})
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})
    else:
        context = {'base_template': 'main/base_visitor.html'}

    annuncio = Annuncio.objects.filter(id=oid).first()
    context['annuncio'] = annuncio
    context['annuncio_utente'] = annuncio.user
    context['annuncio_profilo'] = Profile.objects.filter(user=annuncio.user).first()
    context['annuncio_accetta_profilo'] = Profile.objects.filter(user=annuncio.user_accetta).first()
    context['annuncio_utente_recensioni'] = Recensione.objects.filter(user_recensito=annuncio.user).count()
    context['annuncio_utente_voti'] = Recensione.objects.all().filter(user_recensito=annuncio.user)\
        .aggregate(Avg('voto'))
    context['annuncio_servizi'] = Servizio.objects.filter(annuncio=annuncio).first()

    return render(request, 'annunci/dettagli_annuncio.html', context)


@login_required(login_url='/utenti/login/')
def elimina_annuncio(request, oid):
    """
    Mostra una pagina di conferma eliminazione dell'annuncio.

    :param request: request utente.
    :param oid: l'id dell'annuncio da eliminare.
    :return: render di conferma elimina_annuncio o redirect alla home.
    """

    annuncio = Annuncio.objects.filter(id=oid).first()
    if annuncio.user == request.user:
        context = {'annuncio': annuncio, 'base_template': 'main/base.html',
                   'user_profile': Profile.objects.filter(user=request.user).first()}

        return render(request, 'annunci/elimina_annuncio.html', context)

    return HttpResponseRedirect(reverse('main:index'))


@login_required(login_url='/utenti/login/')
def elimina_annuncio_conferma(request, oid):
    """
    Elimina l'annuncio.

    :param request: request utente.
    :param oid: l'id dell'annuncio da eliminare.
    :return: redirect alla home.
    """

    annuncio = Annuncio.objects.filter(id=oid).first()

    if annuncio.user == request.user:
        Annuncio.objects.filter(id=oid).first().logo_annuncio.delete(save=True)
        if not annuncio.annuncio_petsitter:
            userprofile = Profile.objects.filter(user=request.user).first()
            userprofile.pet_coins = userprofile.pet_coins + annuncio.pet_coins
            userprofile.save()

        Annuncio.objects.filter(id=oid).delete()

    return HttpResponseRedirect(reverse('main:index'))


@login_required(login_url='/utenti/login/')
def inserisci_annuncio(request):
    """
    Permette all'utente di inserire un nuovo annuncio.

    :param request: request utente.
    :return: render pagina inserisci_annuncio e redirect alla home.
    """

    form = AnnuncioForm(request.POST or None, request.FILES or None)
    servizioform = ServizioForm(request.POST or None)

    context = {
        "form": form,
        "servizioForm": servizioform,
    }

    if form.is_valid() and servizioform.is_valid():
        userprofile = Profile.objects.filter(user=request.user).first()

        msg = controllo_pet_coins(userprofile, form.cleaned_data['pet_coins'])
        if msg is not True:
            context = {
                'form': form,
                'servizioForm': servizioform,
                'error_message': msg,
                'user_profile': userprofile,
                'base_template': 'main/base.html',
            }
            return render(request, 'annunci/inserisci_annuncio.html', context)

        if not userprofile.pet_sitter and form.cleaned_data['pet_coins'] > userprofile.pet_coins:
            context.update({'error_message': 'Errore: pet coins insufficienti per inserire l\'annuncio'})
        else:
            annuncio = Annuncio.objects.create(user=request.user)
            if not userprofile.pet_sitter:
                userprofile.pet_coins = userprofile.pet_coins - form.cleaned_data['pet_coins']
                userprofile.save()

            if userprofile.pet_sitter:
                annuncio.annuncio_petsitter = True
            else:
                annuncio.annuncio_petsitter = False

            annuncio.titolo = form.cleaned_data['titolo']
            annuncio.sottotitolo = form.cleaned_data['sottotitolo']
            annuncio.descrizione = form.cleaned_data['descrizione']
            annuncio.pet = form.cleaned_data['pet']
            annuncio.pet_coins = form.cleaned_data['pet_coins']
            annuncio.data_inizio = form.cleaned_data['data_inizio']
            annuncio.data_fine = form.cleaned_data['data_fine']

            try:
                annuncio.logo_annuncio = form.cleaned_data['logo_annuncio']
            except Exception:
                annuncio.logo_annuncio = None

            annuncio.save()

            servizi = Servizio.objects.create(annuncio=annuncio)
            servizi.passeggiate = servizioform.cleaned_data['passeggiate']
            servizi.pulizia_gabbia = servizioform.cleaned_data['pulizia_gabbia']
            servizi.ore_compagnia = servizioform.cleaned_data['ore_compagnia']
            servizi.cibo = servizioform.cleaned_data['cibo']
            servizi.accompagna_dal_vet = servizioform.cleaned_data['accompagna_dal_vet']
            servizi.save()

            return HttpResponseRedirect(reverse('main:index'))

    context.update({'base_template': 'main/base.html'})
    context.update({'user_profile': Profile.objects.filter(user=request.user).first()})

    return render(request, 'annunci/inserisci_annuncio.html', context)


def lista_annunci(request):
    """
    Mostra all'utente la lista degli annunci aperti.

    :param request: request utente.
    :return: render pagina lista_annunci.
    """

    dati = recupera_annunci(request)

    annunci_validi = dati.get('annunci_validi').filter(user_accetta__isnull=True)

    sel_pet = dati.get('sel_pet')
    sel_categoria = dati.get('sel_categoria')
    ordina = dati.get('ordina')
    annunci = dati.get('annunci')
    annunci_recensioni = {}
    annunci_voti = {}

    indici = []
    are_ordinati = False
    if request.user.is_authenticated():
        if ordina != 'non_ordinare':
            user_profile = Profile.objects.filter(user=request.user).first()
            indici = ordina_annunci(user_profile, annunci_validi, ordina)
            are_ordinati = True

    annunci_validi = list(annunci_validi)
    new_annunci_validi = list()
    # Ordina annunci_validi
    if are_ordinati:
        for i, annuncio in enumerate(annunci_validi):
            new_annunci_validi.append(annunci_validi[indici[i]])
        annunci_validi = new_annunci_validi

    for annuncio in annunci_validi:
        annunci[annuncio] = Profile.objects.filter(user=annuncio.user).first()
        annunci_recensioni[annuncio] = Recensione.objects.filter(user_recensito=annuncio.user).count()
        voti = Recensione.objects.all().filter(user_recensito=annuncio.user).aggregate(Avg('voto'))
        if voti.get('voto__avg') is None:
            voti['voto__avg'] = 0

        annunci_voti[annuncio] = voti.get('voto__avg')

    context = {
        'annunci': annunci,
        'sel_categoria': sel_categoria,
        'sel_pet': sel_pet,
        'annunci_voti': annunci_voti,
        'annunci_recensioni': annunci_recensioni,
        'are_ordinati': are_ordinati,
        'indici': indici,
        'ordina': ordina
    }

    if not request.user.is_authenticated():
        context.update({'base_template': 'main/base_visitor.html'})
        return render(request, 'annunci/lista_annunci.html', context)
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        context.update({'base_template': 'main/base.html'})
        context.update({'user_profile': user_profile})
        return render(request, 'annunci/lista_annunci.html', context)


@login_required(login_url='/utenti/login/')
def modifica_annuncio(request, oid):
    """
    Permette all'utente di modificare un annuncio.

    :param request: request utente.
    :param oid: id dell'annuncio da modificare.
    :return: render pagina modifica_annuncio.
    """

    annuncio = Annuncio.objects.filter(id=oid).first()
    servizi = Servizio.objects.filter(annuncio=annuncio).first()
    userprofile = Profile.objects.filter(user=request.user).first()
    pet_coins_iniziali = 0
    context = {}

    if not annuncio.annuncio_petsitter:
        pet_coins_iniziali = annuncio.pet_coins

    form = AnnuncioForm(data=request.POST or None, instance=annuncio, files=request.FILES)
    servizioform = ServizioForm(data=request.POST or None, instance=servizi)

    if form.is_valid() and servizioform.is_valid():

        msg = controllo_pet_coins(userprofile, form.cleaned_data['pet_coins'])
        if msg is not True:
            context = {
                'form': form,
                'servizioForm': servizioform,
                'error_message': msg,
                'user_profile': userprofile,
                'base_template': 'main/base.html',
            }
            return render(request, 'annunci/modifica_annuncio.html', context)

        if not annuncio.annuncio_petsitter:
            costo = form.cleaned_data['pet_coins'] - pet_coins_iniziali
            if costo > userprofile.pet_coins:
                context.update({'error_message': 'Errore: pet coins insufficienti per inserire l\'annuncio'})
            else:
                userprofile.pet_coins = userprofile.pet_coins - costo
                userprofile.save()
                form.save()
                servizioform.save()
                return HttpResponseRedirect(reverse('annunci:lista-annunci'))
        else:
            form.save()
            servizioform.save()
            return HttpResponseRedirect(reverse('annunci:lista-annunci'))
    else:
        form = AnnuncioForm(instance=annuncio)
        servizioform = ServizioForm(instance=servizi)

    context.update({'form': form})
    context.update({'servizioForm': servizioform})
    context.update({'base_template': 'main/base.html'})
    context.update({'user_profile': userprofile})

    return render(request, 'annunci/modifica_annuncio.html', context)


def ordina_annunci(user_profile, annunci_validi, ordina):
    """
    Ordina gli annunci per distanza geografica secondo la selezione fatta dall'utente.

    :param user_profile: profilo utente.
    :param annunci_validi: lista degli annunci che verranno mostrati.
    :param ordina: indica se l'ordinamento deve essere crescente, decrescente o non ordinare.
    :return: indici degli annunci ordinati.
    """

    lat_user = 0
    lng_user = 0
    if user_profile.latitudine is not None and user_profile.longitudine is not None:
        lat_user = user_profile.latitudine
        lng_user = user_profile.longitudine
    distanze = []
    indici = []

    # raggio della terra approssimato, in km
    r = 6373.0

    lat1 = radians(lat_user)
    lon1 = radians(lng_user)

    # Calcola le distanze di tutti gli annunci
    for i, annuncio in enumerate(annunci_validi):
        indici.append(i)
        annuncio_profilo = Profile.objects.filter(user=annuncio.user).first()

        if annuncio_profilo.latitudine is not None and annuncio_profilo.longitudine is not None:
            lat2 = radians(annuncio_profilo.latitudine)
            lon2 = radians(annuncio_profilo.longitudine)
        else:
            lat2 = 0
            lon2 = 0

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distanze.append(r * c)

    # Ordina in base all'order param
    if ordina == 'crescente':
        distanze, indici = (list(t) for t in zip(*sorted(zip(distanze, indici))))

    if ordina == 'decrescente':
        distanze, indici = (list(t) for t in zip(*sorted(zip(distanze, indici), reverse=True)))

    return indici


def recupera_annunci(request):
    """
    Recupera dal model tutti gli annunci che fanno match con le selezioni delle categorie effettuate dall'utente.
    Controlla che gli annunci recuperati siano ancora aperti (non accettati) e con data di scadenza valida.

    :param request: request .
    :return: dati: dizionario contenente gli annunci validi recuperati e la configurazione attuale della view.
    """

    # controllo annunci scaduti non accettati e li elimino
    annunci_validi = Annuncio.objects.all()
    for annuncio in annunci_validi:
        if annuncio.user_accetta is None and annuncio.data_fine < datetime.now(timezone.utc) + timedelta(hours=2):
            # se l'inserzionista è un utente normale, restituisci i suoi pet coins
            temp_profile = Profile.objects.filter(user=annuncio.user).first()
            if not temp_profile.pet_sitter:
                temp_profile.pet_coins = temp_profile.pet_coins + annuncio.pet_coins
                temp_profile.save()
            Annuncio.objects.filter(id=annuncio.id).delete()

    sel_categoria = 'tutte'
    sel_pet = 'tutti'
    ordina = 'non_ordinare'

    if request.POST.get('sel_categoria') is not None:
        sel_categoria = request.POST.get('sel_categoria')
    if request.POST.get('sel_pet') is not None:
        sel_pet = request.POST.get('sel_pet')
    if request.POST.get('ordina') is not None:
        ordina = request.POST.get('ordina')

    annunci = {}

    if sel_categoria == 'petsitter':
        profili_normali = Profile.objects.filter(pet_sitter=False)
        id_list = []
        for profilo in profili_normali:
            id_list.append(profilo.user.id)

        utenti = User.objects.exclude(id__in=id_list)

        annunci_validi = Annuncio.objects.filter(user__in=utenti)
    else:
        if sel_categoria == 'normale':
            profili_petsitter = Profile.objects.filter(pet_sitter=True)
            id_list = []
            for profilo in profili_petsitter:
                id_list.append(profilo.user.id)

            utenti = User.objects.exclude(id__in=id_list)

            annunci_validi = Annuncio.objects.filter(user__in=utenti)
        else:
            sel_categoria = 'tutte'
            annunci_validi = Annuncio.objects.all()

    if sel_pet is not None:
        if sel_pet != 'tutti':
            annunci_validi = annunci_validi.filter(pet=sel_pet)
    else:
        sel_pet = 'tutti'

    dati = {'annunci_validi': annunci_validi, 'sel_pet': sel_pet, 'sel_categoria': sel_categoria, 'annunci': annunci,
            'ordina': ordina}

    return dati
