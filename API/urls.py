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

    # /API/utenti/profilo/<int:oid> metodi ammessi :GET / PUT
    url(r'utenti/profilo/(?P<pk>[0-9]+)/$', views.userInfoLogin.as_view(), name='API-user-info'),

    # /API/utenti/profilo/<int:oid>/anagrafica   metodi ammessi : GET / PUT
    # url(r'utenti/profilo/(?P<pk>[0-9]+)/anagrafica/$', views.anagraficaUtente.as_view(), name='API-anagrafica-utente'),

    # /API/annunci/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/$', views.listaAnnunci.as_view(), name='API-lista-annunci'),

    # /API/annunci/filtra-per-cane/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-cane/$', views.filtraAnnunciPerCane.as_view(), name='API-filtra-annunci-per-cane'),

    # /API/annunci/filtra-per-gatto/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-gatto/$', views.filtraAnnunciPerGatto.as_view(), name='API-filtra-annunci-per-gatto'),

    # /API/annunci/filtra-per-coniglio/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-coniglio/$', views.filtraAnnunciPerConiglio.as_view(),
        name='API-filtra-annunci-per-coniglio'),

    # /API/annunci/filtra-per-volatile/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-volatile/$', views.filtraAnnunciPerVolatile.as_view(),
        name='API-filtra-annunci-per-volatile'),

    # /API/annunci/filtra-per-rettile/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-rettile/$', views.filtraAnnunciPerRettile.as_view(),
        name='API-filtra-annunci-per-rettile'),

    # /API/annunci/filtra-per-altro/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-altro/$', views.filtraAnnunciPerAltro.as_view(),
        name='API-filtra-annunci-per-altro'),

    # /API/annunci/filtra-per-petsitter/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-petsitter/$', views.filtraAnnunciPetsitter.as_view(),
        name='API-filtra-annunci-petsitter'),

    # /API/annunci/filtra-per-petsitter/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/filtra-per-utenti-normali/$', views.filtraAnnunciUtentiNormali.as_view(),
        name='API-filtra-annunci-utenti-normali'),

    # /API/annunci/ordina-per-dist-crescente/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/ordina-per-dist-crescente/$', views.ordinaAnnunciDistanzaCrescente.as_view(),
        name='API-ordina-annunci-distanza-crescente'),

    # /API/annunci/filtra-per-dist-decrescente/  metodi ammessi  GET : a tutti gli utenti
    url(r'annunci/ordina-per-dist-decrescente/$', views.ordinaAnnunciDistanzaDecrescente.as_view(),
        name='API-ordina-annunci-distanza-decrescente'),

    # /API/annunci/<int:oid>/dettagli' GET : a tutti gli utenti | POST/PUT/DELETE solo ai proprietari
    url(r'annunci/(?P<pk>[0-9]+)/dettagli/$', views.dettaglioAnnuncio.as_view(), name='API-dettaglio-annuncio'),

    # /API/annunci/<int:oid>/flag' GET : a tutti gli utenti | POST/PUT/DELETE solo ai proprietari
    # url(r'annunci/(?P<pk>[0-9]+)/servizirichiesti/$', views.servizi_richiesti.as_view(), name='API-flag-annuncio'),

    # /API/annunci/<int:oid>/elenco' GET : a tutti gli utenti
    url(r'annunci/(?P<pk>[0-9]+)/elenco/$', views.elencoAnnunciUtente.as_view(), name='API-elenco-annunci-utente'),

    # /API/annunci/nuovo/
    url(r'annunci/nuovo/$', views.inserisciAnnuncio.as_view(), name='API-nuovo-annuncio'),

    # # /API/annunci/nuovo/
    # url(r'annunci/nuovo-con-servizi/$', views.inserisciAnnuncioConServizi.as_view(), name='API-nuovo-con-servizi'),

    # /API/annunci/<int:oid>/dettagli' GET : a tutti gli utenti | POST/PUT/DELETE solo ai proprietari
    url(r'annunci/(?P<pk>[0-9]+)/accetta/$', views.accettaAnnuncio.as_view(), name='API-accetta-annuncio'),


    # /API/annunci/<int:oid>/elenco' GET : a tutti gli utenti
    url(r'annunci/calendario/$', views.calendarioUtente.as_view(), name='API-calendario-utente'),

    # /API/utenti/cerca/<char:name>' GET : tutti gli utenti
    url(r'utenti/cerca/(?P<name>[A-Za-z0-9èòàùì]+)/$', views.cercaUtente.as_view(), name='API-cerca-utente'),

    #
    # # /API/lista-utenti/<int:oid>'
    # url(r'lista-utenti/(?P<oid>[0-9]+)/$', views.UserDetailAPIView.as_view(), name='API-get-user-detail'),
    #
    # # /API/lista-utenti/<int:oid>/profilo'
    # url(r'lista-utenti/(?P<oid>[0-9]+)/profilo', views.ProfileDetailAPIView.as_view(), name='API-get-profile-detail'),
    #
    # # /API/lista-profili/
    # url(r'lista-profili/$', views.ProfileListCreateAPIView.as_view(), name='API-get-lista-profili'),
    # #
    # # # /API/get_users/<int:oid>'
    # # url(r'lista-profili/(?P<oid>[0-9]+)/$', views.ProfileDetailAPIView.as_view(), name='API-get-profile-detail'),
    #


]