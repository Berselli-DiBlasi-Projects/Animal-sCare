from django.conf.urls import url
from . import views

app_name = 'annunci'

urlpatterns = [

    # /annunci/
    url(r'^$', views.lista_annunci, name='lista-annunci'),

    # /annunci/nuovo/
    url(r'nuovo/$', views.inserisci_annuncio, name='inserisci_annuncio'),

    # /annunci/#annuncio/
    url(r'(?P<oid>[0-9]+)/$', views.dettagli_annuncio, name='dettagli_annuncio'),

    # /annuncio/#annuncio/modifica/
    url(r'(?P<oid>[0-9]+)/modifica/$', views.modifica_annuncio, name='modifica_annuncio'),

    # /annuncio/#annuncio/elimina/
    url(r'(?P<oid>[0-9]+)/elimina/$', views.elimina_annuncio, name='elimina_annuncio'),

    # /annuncio/#annuncio/accetta/
    url(r'(?P<oid>[0-9]+)/accetta/$', views.accetta_annuncio, name='accetta_annuncio'),

    # /annuncio/#annuncio/accetta/conferma/
    url(r'(?P<oid>[0-9]+)/accetta/conferma/$', views.conferma_annuncio, name='conferma_annuncio'),

    # /annunci/calendario/
    url(r'calendario/$', views.calendario, name='calendario'),

    # /annunci/@username/
    url(r'(?P<username>\w+)/$', views.annunci_di_utente, name='annunci_di_utente'),
]
