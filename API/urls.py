from django.conf.urls import url
from . import views

app_name = 'API'

urlpatterns = [

########################################################################################################################
    # DA ELIMINARE
    url(r'lista-anagrafica/$', views.ListaAnagraficheRegistrate.as_view(), name='API-Lista-Anagrafiche'),

    # # DA ELIMINARE
    url(r'lista-profili/$', views.ListaUtentiRegistrati.as_view(), name='API-lista-profili-utente'),

    # # DA ELIMINARE
    url(r'lista-servizi/$', views.elencoservizi.as_view(), name='API-elencoservizi'),

########################################################################################################################

    # prende le informazioni di un utente
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET
    url(r'utenti/profilo/(?P<pk>[0-9]+)/$', views.userInfoLogin.as_view(), name='API-user-info'),

    # prende le informazioni dell'utente che ha richiamato l'api e ne permette la modifica
    # /API/utenti/profilo/<int:oid> metodi ammessi :GET / PUT
    url(r'utenti/profilo/$', views.selfUserInfoLogin.as_view(), name='API-self-user-info'),

    # completa la registrazione per un petsitter
    # /API/utenti/registra/petsitter metodi ammessi :PUT
    url(r'utenti/registra/petsitter$', views.completaRegPetsitter.as_view(), name='API-registra-petsitter'),

    # completa la registrazione per un utente normale
    # /API/utenti/registra/utente-normale metodi ammessi :PUT
    url(r'utenti/registra/utente-normale$', views.completaRegUtentenormale.as_view(),
        name='API-registra-utente-normale'),

    # visualizza gli annunci
    # /API/annunci/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/$', views.listaAnnunci.as_view(), name='API-lista-annunci'),

    # filtra gli annunci
    # /API/annunci/filtra-per-dist-decrescente/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/ordina/(?P<animale>[A-Za-z0-9*èòàùì]+)/(?P<ordinamento>[A-Za-z0-9*èòàùì]+)/(?P<tipo_utente>[A-Za-z0-9*èòàùì]+)/$',
        views.ordinaAnnunci.as_view(),
        name='API-ordina-annunci-distanza-decrescente'),

    # osserva l'annuncio nel dettaglio e ne permette anche l'eliminazione o modifica purchè chi la chiama è
    # colui che lo ha scritto
    # /API/annunci/<int:oid>/dettagli' GET : a tutti gli utenti | POST/PUT/DELETE solo ai proprietari
    url(r'annunci/(?P<pk>[0-9]+)/dettagli/$', views.dettaglioAnnuncio.as_view(), name='API-dettaglio-annuncio'),

    # restituisce solamente gli annunci di un utente avente un determinato ID
    # /API/annunci/<int:oid>/elenco' GET : a tutti gli utenti
    url(r'annunci/(?P<pk>[0-9]+)/elenco/$', views.elencoAnnunciUtente.as_view(), name='API-elenco-annunci-utente'),

    # inserisce un nuovo annuncio
    # /API/annunci/nuovo/
    url(r'annunci/nuovo/$', views.inserisciAnnuncio.as_view(), name='API-nuovo-annuncio'),

    # accetta un annuncio avente ID comunicato via link
    # /API/annunci/<int:oid>/dettagli' GET : a tutti gli utenti | POST/PUT/DELETE solo ai proprietari
    url(r'annunci/(?P<pk>[0-9]+)/accetta/$', views.accettaAnnuncio.as_view(), name='API-accetta-annuncio'),

    # restituisce gli annunci accettati dall'utente che richiama questo link
    # /API/annunci/<int:oid>/elenco' GET : a tutti gli utenti
    url(r'annunci/calendario/$', views.calendarioUtente.as_view(), name='API-calendario-utente'),

    # cerca l'utente per username
    # /API/utenti/cerca/<char:name>' GET : tutti gli utenti
    url(r'utenti/cerca/(?P<name>[A-Za-z0-9èòàùì]+)/$', views.cercaUtente.as_view(), name='API-cerca-utente'),

    # classifica utenti
    # /API/utenti/classifica/<tipo utente>/<criterio>/  metodi ammessi  GET : a tutti gli utenti
    url(r'utenti/classifica/(?P<tipo_utente>[A-Za-z0-9*èòàùì]+)/(?P<criterio>[A-Za-z0-9èòàùì]+)/$',
        views.classificaUtenti.as_view(),
        name='API-classifica-utenti'),

    # Cassa Pet Coins utenti
    # /API/utenti/cassa/<quantità>/  metodi ammessi  GET : a tutti gli utenti
    url(r'utenti/cassa/$',
        views.modificaPetCoins.as_view(),
        name='API-petcoins-utenti'),

    # recensisci utenti
    # recensioni/nuova/<utente_recensito>/<utente_recensore>/ metodi ammessi  GET : a tutti gli utenti
    url(r'recensioni/nuova/(?P<utente>[A-Za-z0-9èòàùì]+)/$',
        views.recensisciUtente.as_view(),
        name='API-recensisci-utenti'),

    # recensioni di un utente
    # /API/recensioni/ricevute/<utente>/  metodi ammessi  GET : a tutti gli utenti
    url(r'recensioni/ricevute/(?P<utente>[A-Za-z0-9èòàùì]+)/$',
        views.recensioniRicevute.as_view(),
        name='API-lista-recensioni-utente'),

    # modifica una recensione fatta per un utente
    # /API/recensioni/ricevute/<utente>/  metodi ammessi  GET : a tutti gli utenti
    url(r'recensioni/modifica/(?P<utente>[A-Za-z0-9èòàùì]+)/$',
        views.modificaRecensione.as_view(),
        name='API-modifica-recensione'),

    # contattaci
    # /API/annunci/nuovo/
    url(r'contattaci/$', views.contattaciInPrivato.as_view(), name='API-contattaci'),
]