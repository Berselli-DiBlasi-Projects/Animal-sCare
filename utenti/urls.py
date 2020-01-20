from django.conf.urls import url
from . import views

app_name = 'utenti'

urlpatterns = [

    # /utenti/login/
    url(r'login/$', views.login_user, name='utenti-login'),

    # /utenti/registrazione/
    url(r'registrazione/$', views.registrazione, name='registrazione'),

    # /utenti/registrazione/normale
    url(r'registrazione/normale$', views.registrazione_normale, name='registrazione-normale'),

    # /utenti/registrazione/petsitter
    url(r'registrazione/petsitter$', views.registrazione_petsitter, name='registrazione-petsitter'),

    # /utenti/logout/
    url(r'logout/$', views.logout_user, name='utenti-logout'),

    # /utenti/profilo/#user
    url(r'profilo/(?P<oid>[0-9]+)/$', views.view_profile, name='view-profile'),

    # /utenti/profilo/#user/modifica/
    url(r'profilo/(?P<oid>[0-9]+)/modifica/$', views.edit_profile, name='edit-profile'),

    # /utenti/profilo/#user/elimina/
    url(r'(?P<oid>[0-9]+)/elimina/$', views.elimina_profilo, name='elimina_profilo'),

    # /utenti/profilo/#user/elimina/conferma/
    url(r'(?P<oid>[0-9]+)/elimina/conferma/$', views.elimina_profilo_conferma, name='elimina_profilo_conferma'),

    # /utenti/cassa/
    url(r'cassa/$', views.cassa, name='cassa'),

    # /utenti/classifica/
    url(r'classifica/$', views.classifica, name='classifica'),

    # /utenti/cerca/
    url(r'cerca/$', views.cerca_utenti, name='cerca_utenti'),

    # /check_username/?username=john
    url(r'check_username/$', views.check_username, name='check_username'),

#     modifica per la google auth
#     /utenti/scegli_profilo/
    url(r'scegli_profilo/$', views.scelta_profilo_oauth, name='scelta_profilo_oauth'),

#     /utenti/oauth_petsitter
    url(r'oauth_petsitter/$', views.oauth_petsitter, name='oauth_petsitter'),

#     /utenti/oauth_normale
    url(r'oauth_normale/$', views.oauth_normale, name='oauth_normale'),
]
