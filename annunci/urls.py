from django.conf.urls import url
from . import views

app_name = 'annunci'

urlpatterns = [

    # /annunci/
    url(r'^$', views.lista_annunci, name='lista-annunci'),

    # /annunci/nuovo/
    url(r'nuovo/$', views.inserisci_annuncio, name='inserisci_annuncio'),

    # /annunci/#annuncio/dettagli/
    url(r'(?P<oid>[0-9]+)/dettagli/$', views.dettagli_annuncio, name='dettagli_annuncio'),

    # /annunci/#annuncio/modifica/
    url(r'(?P<oid>[0-9]+)/modifica/$', views.modifica_annuncio, name='modifica_annuncio'),

    # /annunci/#annuncio/elimina/
    url(r'(?P<oid>[0-9]+)/elimina/$', views.elimina_annuncio, name='elimina_annuncio'),

    # /annunci/#annuncio/elimina/conferma/
    url(r'(?P<oid>[0-9]+)/elimina/conferma/$', views.elimina_annuncio_conferma, name='elimina_annuncio_conferma'),

    # /annunci/#annuncio/accetta/
    url(r'(?P<oid>[0-9]+)/accetta/$', views.accetta_annuncio, name='accetta_annuncio'),

    # /annunci/#annuncio/accetta/conferma/
    url(r'(?P<oid>[0-9]+)/accetta/conferma/$', views.conferma_annuncio, name='conferma_annuncio'),

    # /annunci/calendario/
    url(r'calendario/$', views.calendario, name='calendario'),

    # /annunci/@username/elenco
    url(r'(?P<username>\w+)/elenco/$', views.annunci_di_utente, name='annunci_di_utente'),
]
