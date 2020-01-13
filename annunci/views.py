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
import re

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/utenti/login/')
def accetta_annuncio(request, oid):
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
                                                                      'login su Animal\'sCare per controllare subito!',
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

    if not request.user.is_authenticated():
        return render(request, 'annunci/lista_annunci.html', {'base_template': 'main/base_visitor.html',
                                                              'annunci': annunci,
                                                              'sel_categoria': sel_categoria,
                                                              'sel_pet': sel_pet,
                                                              'annunci_voti': annunci_voti,
                                                              'annunci_recensioni': annunci_recensioni,
                                                              'username': username})
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        return render(request, 'annunci/lista_annunci.html', {'base_template': 'main/base.html',
                                                              'user_profile': user_profile,
                                                              'annunci': annunci,
                                                              'sel_categoria': sel_categoria,
                                                              'sel_pet': sel_pet,
                                                              'annunci_voti': annunci_voti,
                                                              'annunci_recensioni': annunci_recensioni,
                                                              'username': username})


@login_required(login_url='/utenti/login/')
def calendario(request):
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

    return render(request, 'annunci/calendario.html', {'base_template': 'main/base.html',
                                                       'user_profile': user_profile,
                                                       'annunci': annunci,
                                                       'sel_categoria': sel_categoria,
                                                       'sel_pet': sel_pet,
                                                       'annunci_voti': annunci_voti,
                                                       'annunci_recensioni': annunci_recensioni})


@login_required(login_url='/utenti/login/')
def conferma_annuncio(request, oid):
    annuncio = Annuncio.objects.filter(id=oid).first()
    context = {'annuncio': annuncio, 'base_template': 'main/base.html',
               'user_profile': Profile.objects.filter(user=request.user).first()}

    return render(request, 'annunci/conferma_annuncio.html', context)


def controllo_form_annuncio(userprofile, form):
    # controllo titolo
    if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", form.cleaned_data['titolo']):
        return 'Errore: il titolo può contenere solo lettere, numeri e spazi.'
    if not (1 <= len(form.cleaned_data['titolo']) <= 95):
        return 'Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'

    # controllo sottotitolo
    if not re.match("^[A-Za-z0-9 ,.'èòàùì]+$", form.cleaned_data['sottotitolo']):
        return 'Errore: il sottotitolo può contenere solo lettere, numeri, punti, virgole e spazi.'
    if not (1 <= len(form.cleaned_data['sottotitolo']) <= 95):
        return 'Errore: il sottotitolo deve avere lunghezza fra 1 e 95 caratteri.'

    # controllo descrizione
    if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", form.cleaned_data['descrizione']):
        return 'Errore: la descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'
    if not (1 <= len(form.cleaned_data['descrizione']) <= 245):
        return 'Errore: il titolo deve avere lunghezza fra 1 e 245 caratteri.'

    # controllo se data inizio < data_fine e se data_inizio e data_fine > adesso
    data_inizio = form.cleaned_data['data_inizio']
    data_fine = form.cleaned_data['data_fine']
    if data_inizio >= data_fine:
        return 'Errore: la data di inizio deve avvenire prima della data di fine e non possono essere uguali.'
    if data_inizio < datetime.now(timezone.utc) + timedelta(hours=2):
        return 'Errore: la data di inizio non può essere nel passato.'
    if data_fine < datetime.now(timezone.utc) + timedelta(hours=2):
        return 'Errore: la data di fine non può essere nel passato.'

    # controllo pet_coins
    if not re.match("^[0-9]+$", str(form.cleaned_data['pet_coins'])):
        return 'Errore: il campo pet coins può contenere solo numeri.'
    if not (1 <= int(form.cleaned_data['pet_coins']) <= 100000):
        return 'Errore: il valore in pet coins deve essere compreso tra 1 e 100000.'

    # controllo pet_coins sul saldo profilo
    if not userprofile.pet_sitter and userprofile.pet_coins < int(form.cleaned_data['pet_coins']):
        return 'Errore: verifica di avere un saldo in pet coins sufficiente per inserire l\'annuncio.'

    return True


def dettagli_annuncio(request, oid):
    if request.user.is_authenticated():
        context = {'base_template': 'main/base.html'}
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
    Annuncio.objects.filter(id=oid).first().logo_annuncio.delete(save=True)
    annuncio = Annuncio.objects.filter(id=oid).first()
    if not annuncio.annuncio_petsitter:
        userprofile = Profile.objects.filter(user=request.user).first()
        userprofile.pet_coins = userprofile.pet_coins + annuncio.pet_coins
        userprofile.save()

    Annuncio.objects.filter(id=oid).delete()

    return HttpResponseRedirect(reverse('annunci:lista-annunci'))


@login_required(login_url='/utenti/login/')
def inserisci_annuncio(request):
    form = AnnuncioForm(request.POST or None, request.FILES or None)
    servizioform = ServizioForm(request.POST or None)

    context = {
        "form": form,
        "servizioForm": servizioform,
    }

    if form.is_valid() and servizioform.is_valid():
        userprofile = Profile.objects.filter(user=request.user).first()

        msg = controllo_form_annuncio(userprofile, form)
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
                file_type = annuncio.logo_annuncio.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'form': form,
                        'error_message': 'Sono accettate immagini PNG, JPG, o JPEG',
                    }
                    context.update({'base_template': 'main/base.html'})
                    return render(request, 'annunci/inserisci_annuncio.html', context)
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
    dati = recupera_annunci(request)

    annunci_validi = dati.get('annunci_validi').filter(user_accetta__isnull=True)
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

    if not request.user.is_authenticated():
        return render(request, 'annunci/lista_annunci.html', {'base_template': 'main/base_visitor.html',
                                                              'annunci': annunci,
                                                              'sel_categoria': sel_categoria,
                                                              'sel_pet': sel_pet,
                                                              'annunci_voti': annunci_voti,
                                                              'annunci_recensioni': annunci_recensioni})
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        return render(request, 'annunci/lista_annunci.html', {'base_template': 'main/base.html',
                                                              'user_profile': user_profile,
                                                              'annunci': annunci,
                                                              'sel_categoria': sel_categoria,
                                                              'sel_pet': sel_pet,
                                                              'annunci_voti': annunci_voti,
                                                              'annunci_recensioni': annunci_recensioni})


@login_required(login_url='/utenti/login/')
def modifica_annuncio(request, oid):
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

        msg = controllo_form_annuncio(userprofile, form)
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


def recupera_annunci(request):
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

    if request.POST.get('sel_categoria') is not None:
        sel_categoria = request.POST.get('sel_categoria')
    if request.POST.get('sel_pet') is not None:
        sel_pet = request.POST.get('sel_pet')

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

    dati = {'annunci_validi': annunci_validi, 'sel_pet': sel_pet, 'sel_categoria': sel_categoria, 'annunci': annunci}

    return dati
