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
from django.http import HttpResponse
from django.http import Http404
from main.views import nega_accesso_senza_profilo
import operator
import requests

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def calcola_lat_lon(request, profile):
    """
    Dato il profilo di un utente con i dati relativi alla sua residenza, viene fatta una query a un API esterna che
    recupera latitudine e longitudine relative alla posizione dell'utente.

    :param request: request utente.
    :param profile: profilo utente.
    :return: latitudine, longitudine restituite dall'API.
    """

    response = requests.get('https://open.mapquestapi.com/geocoding/v1/address?'
                            'key=REupVcNAuHmBALQsTjMWgMVfp5G5hltJ&location=' + profile.indirizzo.replace("/", "")
                            + ',' + profile.citta.replace("/", "") + ',' + profile.provincia.replace("/", "") +
                            ',' + profile.regione.replace("/", ""))
    latlong = response.json()
    return latlong['results'][0]['locations'][0]['latLng']["lat"], \
        latlong['results'][0]['locations'][0]['latLng']["lng"]


@login_required(login_url='/utenti/login/')
def cassa(request):
    """
    Mostra la pagina cassa, dove l'utente può acquistare Pet coins (simulato nell'app).

    :param request: request utente.
    :return: render della pagina cassa.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    profile = Profile.objects.filter(user=request.user).first()
    context = {'base_template': 'main/base.html'}
    context.update({'user_profile': profile})

    if request.POST.get("value") is not None:
        value = int(request.POST.get("value"))
        if value == 50 or value == 100 or value == 200 or value == -50 or value == -100 or value == -200:
            pet_coins_attuali = profile.pet_coins + value
            if pet_coins_attuali >= 0:
                if pet_coins_attuali <= 10000:
                    profile.pet_coins = pet_coins_attuali
                    profile.save()
                else:
                    context.update({'error_message': 'Errore: hai raggiunto il limite massimo di Pet Coins'})
            else:
                context.update({'error_message': 'Errore: fondi insufficienti'})

    return render(request, 'utenti/cassa.html', context)


def cerca_utenti(request):
    """
    Funzione di ricerca utenti tramite lo username.

    :param request: request utente.
    :return: render della pagina cerca_utenti contenente gli utenti trovati con lo username specificato.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    utenti = User.objects.filter(username__icontains=request.GET.get('cerca'))

    # Escludi dall'elenco gli utenti oauth che non hanno completato il profilo
    for utente in utenti:
        if Profile.objects.filter(user=utente.pk).first() is None:
            utenti = utenti.exclude(pk=utente.pk)

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


def check_username(request):
    """
    Controlla se uno username passato come parametro GET non sia già registrato nel model.

    :param request: request utente.
    :return: False (username già registrato), True (username non registrato).
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    if request.method == "GET":
        p = request.GET.copy()
        if 'username' in p:
            name = p['username']
            if name == request.user.username:
                return HttpResponse(True)
            if User.objects.filter(username__iexact=name):
                return HttpResponse(False)
            else:
                return HttpResponse(True)


def classifica(request):
    """
    Mostra la classifica degli utenti con possibilità di mostrare solo gli account normali o solo gli account dei
    petsitter e la possibilità di ordinare per voto medio o per numero di recensioni ricevute.

    :param request: request utente.
    :return: render della classifica.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

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

    # Escludi dall'elenco gli utenti oauth che non hanno completato il profilo
    for utente in utenti:
        if Profile.objects.filter(user=utente.pk).first() is None:
            utenti = utenti.exclude(pk=utente.pk)

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


@login_required(login_url='/utenti/login/')
def edit_profile(request, oid):
    """
    Permette agli utenti di modificare il proprio profilo, cambiando i loro dati.

    :param request: request utente.
    :param oid: id dell'utente di cui si vuole modificare il profilo (con controllo che sia == all'id
    dell'utente loggato).
    :return: render pagina modifica profilo o errore 404.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    context = {'base_template': 'main/base.html'}
    oaut_user = False
    if int(oid) == int(request.user.pk):
        user_profile = User.objects.filter(id=oid).first()
        if user_profile.has_usable_password():
            form = UserForm(data=request.POST or None, instance=request.user, oauth_user=0)
        else:
            form = UserForm(data=request.POST or None, instance=request.user, oauth_user=1)
            oaut_user = True

        profile = Profile.objects.filter(user=user_profile.pk).first()

        if not profile.pet_sitter:
            profile_form = UtenteNormaleForm(data=request.POST or None, instance=profile, files=request.FILES)
        else:
            profile_form = UtentePetSitterForm(data=request.POST or None, instance=profile, files=request.FILES)

        if form.is_valid() and profile_form.is_valid():

            if not oaut_user:
                if form.cleaned_data['password'] != form.cleaned_data['conferma_password']:
                    context.update({'form': form})
                    context.update({'profileForm': profile_form})
                    context.update({'error_message': 'Errore: le due password inserite non corrispondono'})

                    return render(request, 'utenti/modifica_profilo.html', context)

            profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)

            user = form.save(commit=False)
            if not oaut_user:
                password = form.cleaned_data['password']
                user.set_password(password)
            form.save()
            profile_form.save()
            if not oaut_user:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                if user.is_active:
                    if not oaut_user:
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
                # Nessun utente trovato con questo username --> username valido
                pass

            if oaut_user:
                form = UserForm(instance=request.user, oauth_user=1)
            else:
                form = UserForm(instance=request.user, oauth_user=0)

            if not profile.pet_sitter:
                profile_form = UtenteNormaleForm(instance=profile)
            else:
                profile_form = UtentePetSitterForm(instance=profile)

        context.update({'form': form})
        context.update({'profileForm': profile_form})
        context['user_profile'] = profile

        return render(request, 'utenti/modifica_profilo.html', context)

    else:
        raise Http404


@login_required(login_url='/utenti/login/')
def elimina_profilo(request, oid):
    """
    Permette agli utenti di eliminare il proprio profilo, mostrando prima una pagina di conferma.

    :param request: request utente.
    :param oid: id dell'utente da eliminare (con controllo che sia == all'id dell'utente loggato).
    :return: render della pagina elimina_profilo.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    user = User.objects.filter(id=oid).first()
    if user == User.objects.get(username=request.user):
        context = {'user': user, 'base_template': 'main/base.html'}

        return render(request, 'utenti/elimina_profilo.html', context)
    else:
        raise Http404


@login_required(login_url='/utenti/login/')
def elimina_profilo_conferma(request, oid):
    """
    Dopo aver confermato, elimina effettivamente il profilo utente.

    :param request: request utente.
    :param oid: id dell'utente da eliminare.
    :return: render della pagina principale.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    user = User.objects.filter(id=oid).first()

    if user == User.objects.get(username=request.user):
        User.objects.filter(id=oid).delete()
    else:
        raise Http404

    return HttpResponseRedirect(reverse('main:index'))


def login_user(request):
    """
    Permette agli utenti di effettuare il login.

    :param request: request utente.
    :return: render della pagina login.
    """

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
    """
    Permette agli utenti di effettuare il logout.

    :param request: request utente.
    :return: render della pagina principale.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    logout(request)
    return HttpResponseRedirect(reverse('main:index'))


@login_required(login_url='/utenti/login/')
def oauth_normale(request):
    """
    Permette agli utenti di creare un profilo normale utilizzando il login con Oauth di Google.

    :param request: request utente.
    :return: render della pagina di creazione profilo normale.
    """

    try:
        # Se questo utente ha già un profilo, viene rediretto alla home, altrimenti può registrarne uno nuovo
        Profile.objects.get(user=request.user.id)
        return HttpResponseRedirect(reverse('main:index'))
    except Exception:
        pass

    # Se la richiesta è di tipo POST, allora possiamo processare i dati
    if request.method == "POST":
        # Creiamo l'istanza del form e la popoliamo con i dati della POST request (processo di "binding")
        normaleform = UtenteNormaleForm(request.POST, request.FILES)

        if normaleform.is_valid():
            # a questo punto possiamo usare i dati validi
            utente_loggato = User.objects.get(id=request.user.id)
            profile = Profile.objects.get_or_create(user=utente_loggato)
            profile = profile[0]
            try:
                profile.foto_profilo = request.FILES['foto_profilo']
            except Exception:
                profile.foto_profilo = None

            profile.indirizzo = normaleform.cleaned_data['indirizzo']
            profile.citta = normaleform.cleaned_data['citta']
            profile.provincia = normaleform.cleaned_data['provincia']
            profile.regione = normaleform.cleaned_data['regione']
            profile.telefono = normaleform.cleaned_data['telefono']
            profile.nome_pet = normaleform.cleaned_data['nome_pet']
            profile.pet = normaleform.cleaned_data['pet']
            profile.razza = normaleform.cleaned_data['razza']
            profile.eta = normaleform.cleaned_data['eta']
            profile.caratteristiche = normaleform.cleaned_data['caratteristiche']
            try:
                profile.foto_pet = normaleform.cleaned_data['foto_pet']
            except Exception:
                profile.foto_pet = None

            profile.descrizione = 'Null'
            profile.hobby = 'Null'

            profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)

            profile.save()
            if utente_loggato is not None:
                if utente_loggato.is_active:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        normaleform = UtenteNormaleForm()

    # arriviamo a questo punto se si tratta della prima volta che la pagina viene richiesta(con metodo GET),
    # o se il form non è valido e ha errori
    context = {
        "normaleform": normaleform,
        "base_template": "main/base_oauth.html"
    }
    return render(request, 'utenti/oauth_profilo_normale.html', context)


@login_required(login_url='/utenti/login/')
def oauth_petsitter(request):
    """
    Permette agli utenti di creare un profilo da petsitter utilizzando il login con Oauth di Google.

    :param request: request utente.
    :return: render della pagina di creazione profilo da petsitter.
    """

    try:
        # Se questo utente ha già un profilo, viene rediretto alla home, altrimenti può registrarne uno nuovo
        Profile.objects.get(user=request.user.id)
        return HttpResponseRedirect(reverse('main:index'))
    except Exception:
        pass

    # Se la richiesta è di tipo POST, allora possiamo processare i dati
    if request.method == "POST":
        # Creiamo l'istanza del form e la popoliamo con i dati della POST request (processo di "binding")
        petsitterform = UtentePetSitterForm(request.POST, request.FILES)

        if petsitterform.is_valid():
            # a questo punto possiamo usare i dati validi
            utente_loggato = User.objects.get(id=request.user.id)
            profile = Profile.objects.get_or_create(user=utente_loggato)
            profile = profile[0]

            try:
                profile.foto_profilo = request.FILES['foto_profilo']
            except Exception:
                profile.foto_profilo = None

            profile.indirizzo = petsitterform.cleaned_data['indirizzo']
            profile.citta = petsitterform.cleaned_data['citta']
            profile.provincia = petsitterform.cleaned_data['provincia']
            profile.regione = petsitterform.cleaned_data['regione']
            profile.telefono = petsitterform.cleaned_data['telefono']
            profile.descrizione = petsitterform.cleaned_data['descrizione']
            profile.hobby = petsitterform.cleaned_data['hobby']
            profile.pet_sitter = True
            profile.nome_pet = 'Null'
            profile.pet = 'Null'
            profile.razza = 'Null'
            profile.eta = 0

            profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)

            profile.save()
            if utente_loggato is not None:
                if utente_loggato.is_active:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        petsitterform = UtentePetSitterForm()

    # arriviamo a questo punto se si tratta della prima volta che la pagina viene richiesta(con metodo GET),
    # o se il form non è valido e ha errori
    context = {
        "petsitterform": petsitterform,
        "base_template": "main/base_oauth.html"
    }

    return render(request, "utenti/oauth_profilo_petsitter.html", context)


def registrazione(request):
    """
    Permette agli utenti di registrarsi al sito.

    :param request: request utente.
    :return: render della pagina di registrazione o redirect a pagina principale.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    if not request.user.is_authenticated():
        base_template = 'main/base_visitor.html'
        return render(request, 'utenti/registrazione.html', {'base_template': base_template})
    else:
        return HttpResponseRedirect(reverse('main:index'))


def registrazione_normale(request):
    """
    Permette agli utenti di registrare un account utente normale.

    :param request: request utente.
    :return: render della pagina di registrazione utente normale.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    form = UserForm(request.POST or None, oauth_user=0)
    normaleform = UtenteNormaleForm(request.POST or None, request.FILES or None)

    if form.is_valid() and normaleform.is_valid() and \
            not User.objects.filter(username=form.cleaned_data['username']).exists():

        user = form.save(commit=False)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile.objects.get(user=user)
        try:
            profile.foto_profilo = request.FILES['foto_profilo']
        except Exception:
            profile.foto_profilo = None

        profile.indirizzo = normaleform.cleaned_data['indirizzo']
        profile.citta = normaleform.cleaned_data['citta']
        profile.provincia = normaleform.cleaned_data['provincia']
        profile.regione = normaleform.cleaned_data['regione']
        profile.telefono = normaleform.cleaned_data['telefono']
        profile.nome_pet = normaleform.cleaned_data['nome_pet']
        profile.pet = normaleform.cleaned_data['pet']
        profile.razza = normaleform.cleaned_data['razza']
        profile.eta = normaleform.cleaned_data['eta']
        profile.caratteristiche = normaleform.cleaned_data['caratteristiche']
        try:
            profile.foto_pet = request.FILES['foto_pet']
        except Exception:
            profile.foto_pet = None

        profile.descrizione = 'Null'
        profile.hobby = 'Null'

        profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)
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
    """
    Permette agli utenti di registrare un account utente petsitter.

    :param request: request utente.
    :return: render della pagina di registrazione utente petsitter.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    form = UserForm(request.POST or None, oauth_user=0)
    petsitterform = UtentePetSitterForm(request.POST or None, request.FILES or None)

    if form.is_valid() and petsitterform.is_valid():

        user = form.save(commit=False)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile.objects.get(user=user)
        try:
            profile.foto_profilo = request.FILES['foto_profilo']
        except Exception:
            profile.foto_profilo = None

        profile.indirizzo = petsitterform.cleaned_data['indirizzo']
        profile.citta = petsitterform.cleaned_data['citta']
        profile.provincia = petsitterform.cleaned_data['provincia']
        profile.regione = petsitterform.cleaned_data['regione']
        profile.telefono = petsitterform.cleaned_data['telefono']
        profile.descrizione = petsitterform.cleaned_data['descrizione']
        profile.hobby = petsitterform.cleaned_data['hobby']
        profile.pet_sitter = True
        profile.nome_pet = 'Null'
        profile.pet = 'Null'
        profile.razza = 'Null'
        profile.eta = 0

        profile.latitudine, profile.longitudine = calcola_lat_lon(request, profile)

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


@login_required(login_url='/utenti/login/')
def scelta_profilo_oauth(request):
    """
    Permette agli utenti di scegliere se creare un profilo Oauth normale o da petsitter.

    :param request: request utente.
    :return: render della pagina di scelta Oauth normale o petsitter.
    """

    try:
        Profile.objects.get(user=request.user.id)
        return HttpResponseRedirect(reverse('main:index'))
    except Exception:
        context = {'base_template': 'main/base_oauth.html'}
        return render(request, 'utenti/scelta_utente_oauth.html', context=context)


def view_profile(request, oid):
    """
    Mostra il profilo di un utente, con la possibilità di visualizzare i suoi annunci, le recensioni ricevute e, se
    profilo utente == utente loggato, di modificare o eliminare il proprio profilo.

    :param request: request utente.
    :param oid: id dell'utente di cui mostrare il profilo.
    :return: render della pagina di visualizzazione profilo utente.
    """

    if nega_accesso_senza_profilo(request):
        return HttpResponseRedirect(reverse('utenti:scelta_profilo_oauth'))

    user = User.objects.filter(id=oid).first()
    if user is None:
        raise Http404

    user_profile = Profile.objects.filter(user=user.pk).first()
    if user_profile is None:
        raise Http404

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
