from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import User, Profile
from .forms import UserForm, UtenteNormaleForm, UtentePetSitterForm
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from recensioni.models import Recensione
from django.db.models import Avg
import operator
import re


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required(login_url='/utenti/login/')
def cassa(request):
    profile = Profile.objects.filter(user=request.user).first()
    context = {'base_template': 'main/base.html'}
    context.update({'user_profile': profile})

    if request.POST.get("value") is not None:
        pet_coins_attuali = profile.pet_coins + int(request.POST.get("value"))
        if pet_coins_attuali >= 0:
            profile.pet_coins = pet_coins_attuali
            profile.save()
        else:
            context.update({'error_message': 'Errore: fondi insufficienti'})

    return render(request, 'utenti/cassa.html', context)


def cerca_utenti(request):

    utenti = User.objects.filter(username__icontains=request.GET.get('cerca'))
    profili = {}
    utenti_recensioni = {}
    utenti_voti = {}

    for utente in utenti:
        profili[utente] = Profile.objects.filter(user=utente.pk).first()
        utenti_recensioni[utente] = Recensione.objects.filter(user_recensito=utente.pk).count()
        voti = Recensione.objects.all().filter(user_recensito=utente.pk).aggregate(Avg('voto'))
        if voti.get('voto__avg') is None:
            voti['voto__avg'] = 0

        utenti_voti[utente] = voti.get('voto__avg')

    context = {
        'profili': profili,
        'utenti_recensioni': utenti_recensioni,
        'utenti_voti': utenti_voti,
    }

    if not request.user.is_authenticated():
        context.update({'base_template': 'main/base_visitor.html'})
    else:
        context.update({'base_template': 'main/base.html'})
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})

    return render(request, 'utenti/cerca_utenti.html', context)


def classifica(request):
    sel_utenti = 'tutti'
    sel_filtro = 'voti'

    if request.POST.get('sel_utenti') is not None:
        sel_utenti = request.POST.get('sel_utenti')
    if request.POST.get('sel_filtro') is not None:
        sel_filtro = request.POST.get('sel_filtro')

    utente_iterable = {}
    profilo = {}

    if sel_utenti == 'petsitter':
        profili_normali = Profile.objects.filter(pet_sitter=False)
        id_list = []
        for j in profili_normali:
            id_list.append(j.user.id)

        utenti = User.objects.exclude(id__in=id_list)
    else:
        if sel_utenti == 'normale':
            profili_petsitter = Profile.objects.filter(pet_sitter=True)
            id_list = []
            for j in profili_petsitter:
                id_list.append(j.user.id)

            utenti = User.objects.exclude(id__in=id_list)
        else:
            sel_utenti = 'tutti'
            utenti = User.objects.all()

    utenti_recensioni = {}
    utenti_voti = {}

    for utente in utenti:
        utente_iterable[utente] = User.objects.filter(id=utente.pk).first()
        profilo[utente] = Profile.objects.filter(user=utente.pk).first()
        utenti_recensioni[utente] = Recensione.objects.filter(user_recensito=utente.pk).count()
        voti = Recensione.objects.all().filter(user_recensito=utente.pk).aggregate(Avg('voto'))
        if voti.get('voto__avg') is None:
            voti['voto__avg'] = 0

        utenti_voti[utente] = voti.get('voto__avg')

    utenti_sorted = []
    utenti_profilo_sorted = []
    utenti_voti_sorted = []
    utenti_recensioni_sorted = []

    if sel_filtro == 'recensioni':
        utenti_recensioni_sorted = sorted(utenti_recensioni.items(), key=operator.itemgetter(1), reverse=True)

        for i, utente in enumerate(utenti_recensioni_sorted):
            utenti_sorted.append((utente[0], utente_iterable.get(utente[0])))
            utenti_profilo_sorted.append((utente[0], profilo.get(utente[0])))
            utenti_voti_sorted.append((utente[0], utenti_voti.get(utente[0])))
    else:
        sel_filtro = 'voti'
        utenti_voti_sorted = sorted(utenti_voti.items(), key=operator.itemgetter(1), reverse=True)

        for i, utente in enumerate(utenti_voti_sorted):
            utenti_sorted.append((utente[0], utente_iterable.get(utente[0])))
            utenti_profilo_sorted.append((utente[0], profilo.get(utente[0])))
            utenti_recensioni_sorted.append((utente[0], utenti_recensioni.get(utente[0])))

    context = {
        'sel_utenti': sel_utenti,
        'sel_filtro': sel_filtro,
        'utenti_sorted': utenti_sorted,
        'utenti_profilo_sorted': utenti_profilo_sorted,
        'utenti_voti_sorted': utenti_voti_sorted,
        'utenti_recensioni_sorted': utenti_recensioni_sorted,
    }

    if not request.user.is_authenticated():
        context.update({'base_template': 'main/base_visitor.html'})
    else:
        context.update({'base_template': 'main/base.html'})
        context.update({'user_profile': Profile.objects.filter(user=request.user).first()})

    return render(request, 'utenti/classifica.html', context)


def controllo_form_registrazione(form, normaleform, petsitter):
    # controllo username
    if not re.match("^[A-Za-z0-9]+$", form.cleaned_data['username']):
        return 'Errore: lo username può contenere solo lettere e numeri.'
    if not (3 <= len(form.cleaned_data['username']) <= 15):
        return 'Errore: lo username deve avere lunghezza fra 3 e 15 caratteri.'

    # controllo password
    if not re.match("^[A-Za-z0-9èòàùì]+$", form.cleaned_data['password']):
        return 'Errore: la password può contenere solo lettere minuscole, maiuscole e numeri.'
    if not (3 <= len(form.cleaned_data['password']) <= 20):
        return 'Errore: la password deve avere lunghezza fra 3 e 20 caratteri.'

    # controllo conferma password
    if not re.match("^[A-Za-z0-9èòàùì]+$", form.cleaned_data['conferma_password']):
        return 'Errore: la conferma password può contenere solo lettere minuscole, maiuscole e numeri.'
    if not (3 <= len(form.cleaned_data['conferma_password']) <= 20):
        return 'Errore: la conferma password deve avere lunghezza fra 3 e 20 caratteri.'

    # controllo nome
    if not re.match("^[A-Za-z 'èòàùì]+$", form.cleaned_data['first_name']):
        return 'Errore: il nome può contenere solo lettere.'
    if not (1 <= len(form.cleaned_data['first_name']) <= 30):
        return 'Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'

    # controllo cognome
    if not re.match("^[A-Za-z 'èòàùì]+$", form.cleaned_data['last_name']):
        return 'Errore: il cognome può contenere solo lettere.'
    if not (1 <= len(form.cleaned_data['last_name']) <= 30):
        return 'Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'

    # controllo email
    if not (5 <= len(form.cleaned_data['email']) <= 50):
        return 'Errore: la mail deve essere compresa gra 5 e 50 caratteri.'

    # controllo indirizzo
    if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", normaleform.cleaned_data['indirizzo']):
        return 'Errore: l\'indirizzo può contenere solo lettere, numeri e /.'
    if not (3 <= len(normaleform.cleaned_data['indirizzo']) <= 50):
        return 'Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'

    # controllo citta
    if not re.match("^[A-Za-z 'èòàùì]+$", normaleform.cleaned_data['citta']):
        return 'Errore: il campo città può contenere solo lettere.'
    if not (3 <= len(normaleform.cleaned_data['citta']) <= 50):
        return 'Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'

    # controllo telefono
    if not re.match("^[0-9]+$", normaleform.cleaned_data['telefono']):
        return 'Errore: il telefono può contenere solo numeri.'
    if not (3 <= len(normaleform.cleaned_data['telefono']) <= 30):
        return 'Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'

    if not petsitter:
        # SE E' UN UTENTE NORMALE!
        # controllo nome pet
        if not re.match("^[A-Za-z 'èòàùì]+$", normaleform.cleaned_data['nome_pet']):
            return 'Errore: il nome del pet può contenere solo lettere.'
        if not (3 <= len(normaleform.cleaned_data['nome_pet']) <= 30):
            return 'Errore: il nome del pet deve avere lunghezza fra 3 e 30 caratteri.'

        # controllo razza
        if not re.match("^[A-Za-z -'èòàùì]+$", normaleform.cleaned_data['razza']):
            return 'Errore: la razza del pet può contenere solo lettere e spazi.'
        if not (3 <= len(normaleform.cleaned_data['razza']) <= 30):
            return 'Errore: la razza del pet deve avere lunghezza fra 3 e 30 caratteri.'

        # controllo eta
        if not re.match("^[0-9]+$", str(normaleform.cleaned_data['eta'])):
            return 'Errore: l\'età può contenere solo numeri.'
        if not (0 <= int(normaleform.cleaned_data['eta']) <= 100):
            return 'Errore: l\'età deve essere compresa fra 0 e 100.'

        # controllo caratteristiche
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", normaleform.cleaned_data['caratteristiche']):
            return 'Errore: il campo caratteristiche può contenere solo lettere, numeri, punti, virgole e spazi.'
        if not (1 <= len(normaleform.cleaned_data['caratteristiche']) <= 245):
            return 'Errore: il campo caratteristiche deve avere lunghezza fra 1 e 245 caratteri.'
    else:
        # SE E' UN PETSITTER
        # controllo descrizione
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", normaleform.cleaned_data['descrizione']):
            return 'Errore: il campo descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'
        if not (1 <= len(normaleform.cleaned_data['descrizione']) <= 245):
            return 'Errore: il campo descrizione deve avere lunghezza fra 1 e 245 caratteri.'

        # controllo hobby
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", normaleform.cleaned_data['hobby']):
            return 'Errore: il campo hobby può contenere solo lettere, numeri, punti, virgole e spazi.'
        if not (1 <= len(normaleform.cleaned_data['hobby']) <= 95):
            return 'Errore: il campo hobby deve avere lunghezza fra 1 e 95 caratteri.'

    return True


@login_required(login_url='/utenti/login/')
def edit_profile(request, oid):
    context = {'base_template': 'main/base.html'}

    if int(oid) == int(request.user.pk):
        form = UserForm(data=request.POST or None, instance=request.user)
        user_profile = User.objects.filter(id=oid).first()
        profile = Profile.objects.filter(user=user_profile.pk).first()

        if not profile.pet_sitter:
            profile_form = UtenteNormaleForm(data=request.POST or None, instance=profile, files=request.FILES)
        else:
            profile_form = UtentePetSitterForm(data=request.POST or None, instance=profile, files=request.FILES)

        if form.is_valid() and profile_form.is_valid():

            # args: form, profile form, is user a petsitter
            if not profile.pet_sitter:
                msg = controllo_form_registrazione(form, profile_form, False)
            else:
                msg = controllo_form_registrazione(form, profile_form, True)

            if msg is not True:
                context = {
                    'form': form,
                    'profileForm': profile_form,
                    'error_message': msg,
                    'base_template': 'main/base.html',
                }
                return render(request, 'utenti/modifica_profilo.html', context)

            if form.cleaned_data['password'] != form.cleaned_data['conferma_password']:

                context.update({'form': form})
                context.update({'profileForm': profile_form})
                context.update({'error_message': 'Errore: le due password inserite non corrispondono'})

                return render(request, 'utenti/modifica_profilo.html', context)

            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            form.save()
            profile_form.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:index'))
        else:
            try:
                if User.objects.exclude(pk=request.user.id).get(username=form['username'].value()):
                    context.update({'form': form})
                    context.update({'profileForm': profile_form})
                    context['user_profile'] = profile

                    return render(request, 'utenti/modifica_profilo.html', context)
            except User.DoesNotExist:
                print('nessun utente trovato con questo username, username valido.')

            context.update({'error_message': 'Errore: ricontrolla foto e i campi inseriti'})
            form = UserForm(instance=request.user)
            if not profile.pet_sitter:
                profile_form = UtenteNormaleForm(instance=profile)
            else:
                profile_form = UtentePetSitterForm(instance=profile)

        context.update({'form': form})
        context.update({'profileForm': profile_form})
        context['user_profile'] = profile

        return render(request, 'utenti/modifica_profilo.html', context)
    else:
        return HttpResponseRedirect(reverse('main:index'))


def login_user(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:index'))
                else:
                    return render(request, 'utenti/login.html', {'error_message': 'Il tuo account è stato disattivato'})
            else:
                return render(request, 'utenti/login.html', {'error_message': 'Login invalido'})
        return render(request, 'utenti/login.html')
    else:
        return HttpResponseRedirect(reverse('main:index'))


@login_required(login_url='/utenti/login/')
def logout_user(request):
        logout(request)
        return HttpResponseRedirect(reverse('main:index'))


def registrazione(request):
    if not request.user.is_authenticated():
        base_template = 'main/base_visitor.html'
        return render(request, 'utenti/registrazione.html', {'base_template': base_template})
    else:
        return HttpResponseRedirect(reverse('main:index'))


def registrazione_normale(request):
    form = UserForm(request.POST or None)
    normaleform = UtenteNormaleForm(request.POST or None, request.FILES or None)

    if form.is_valid() and normaleform.is_valid()and \
            not User.objects.filter(username=form.cleaned_data['username']).exists():

        # args: form, profile form, is user a petsitter
        msg = controllo_form_registrazione(form, normaleform, False)
        if msg is not True:
            context = {
                'form': form,
                'profileForm': normaleform,
                'error_message': msg,
                'base_template': 'main/base_visitor.html',
            }
            return render(request, 'utenti/registrazione_normale.html', context)

        user = form.save(commit=False)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)

        profile.foto_profilo = request.FILES['foto_profilo']
        file_type = profile.foto_profilo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'form': form,
                'profileForm': normaleform,
                'error_message': 'Sono accettate immagini PNG, JPG, o JPEG',
            }
            if not request.user.is_authenticated():
                context['base_template'] = 'main/base_visitor.html'
            else:
                context['base_template'] = 'main/base.html'
            return render(request, 'utenti/registrazione_normale.html', context)

        profile.indirizzo = normaleform.cleaned_data['indirizzo']
        profile.citta = normaleform.cleaned_data['citta']
        profile.telefono = normaleform.cleaned_data['telefono']
        profile.nome_pet = normaleform.cleaned_data['nome_pet']
        profile.pet = normaleform.cleaned_data['pet']
        profile.razza = normaleform.cleaned_data['razza']
        profile.eta = normaleform.cleaned_data['eta']
        profile.caratteristiche = normaleform.cleaned_data['caratteristiche']
        profile.foto_pet = request.FILES['foto_pet']
        file_type = profile.foto_pet.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'form': form,
                'profileForm': normaleform,
                'error_message': 'Sono accettate immagini PNG, JPG, o JPEG',
            }
            if not request.user.is_authenticated():
                context['base_template'] = 'main/base_visitor.html'
            else:
                context['base_template'] = 'main/base.html'
            return render(request, 'utenti/registrazione_normale.html', context)

        profile.descrizione = 'Null'
        profile.hobby = 'Null'
        profile.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    context = {
        "form": form,
        "profileForm": normaleform,
    }

    if not request.user.is_authenticated():
        context['base_template'] = 'main/base_visitor.html'
    else:
        return HttpResponseRedirect(reverse('main:index'))

    return render(request, 'utenti/registrazione_normale.html', context)


def registrazione_petsitter(request):
    form = UserForm(request.POST or None)
    petsitterform = UtentePetSitterForm(request.POST or None, request.FILES or None)

    if form.is_valid() and petsitterform.is_valid():

        # args: form, profile form, is user a petsitter
        msg = controllo_form_registrazione(form, petsitterform, True)
        if msg is not True:
            context = {
                'form': form,
                'profileForm': petsitterform,
                'error_message': msg,
                'base_template': 'main/base_visitor.html',
            }
            return render(request, 'utenti/registrazione_petsitter.html', context)

        user = form.save(commit=False)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)

        profile.foto_profilo = request.FILES['foto_profilo']
        file_type = profile.foto_profilo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'form': form,
                'profileForm': petsitterform,
                'error_message': 'Sono accettate immagini PNG, JPG, o JPEG',
            }
            if not request.user.is_authenticated():
                context['base_template'] = 'main/base_visitor.html'
            else:
                context['base_template'] = 'main/base.html'
            return render(request, 'utenti/registrazione_petsitter.html', context)

        profile.indirizzo = petsitterform.cleaned_data['indirizzo']
        profile.citta = petsitterform.cleaned_data['citta']
        profile.telefono = petsitterform.cleaned_data['telefono']
        profile.descrizione = petsitterform.cleaned_data['descrizione']
        profile.hobby = petsitterform.cleaned_data['hobby']
        profile.pet_sitter = True
        profile.nome_pet = 'Null'
        profile.pet = 'Null'
        profile.razza = 'Null'
        profile.eta = 0
        profile.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    context = {
        "form": form,
        "profileForm": petsitterform,
    }

    if not request.user.is_authenticated():
        context['base_template'] = 'main/base_visitor.html'
    else:
        return HttpResponseRedirect(reverse('main:index'))

    return render(request, 'utenti/registrazione_petsitter.html', context)


def view_profile(request, oid):
    user = User.objects.filter(id=oid).first()
    user_profile = Profile.objects.filter(user=user.pk).first()

    recensioni_num = Recensione.objects.filter(user_recensito=user).count()
    voti = Recensione.objects.all().filter(user_recensito=user).aggregate(Avg('voto'))
    if voti.get('voto__avg') is None:
        voti['voto__avg'] = 0

    voto_avg = voti.get('voto__avg')

    context = {
        'view_user': user,
        'user_profile': user_profile,
        'recensioni_num': recensioni_num,
        'voto_avg': voto_avg,
    }

    if request.user.is_authenticated():
        context.update({'base_template': 'main/base.html'})
    else:
        context.update({'base_template': 'main/base_visitor.html'})

    if not user_profile.pet_sitter:
        return render(request, 'utenti/profilo_normale.html', context)
    else:
        return render(request, 'utenti/profilo_petsitter.html', context)
