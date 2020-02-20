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
    # url(r'annunci/calendario/$', views.calendarioUtente.as_view(), name='API-calendario-utente'),



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