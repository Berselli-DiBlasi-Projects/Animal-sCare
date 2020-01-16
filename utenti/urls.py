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

    # /utenti/cassa/
    url(r'cassa/$', views.cassa, name='cassa'),

    # /utenti/classifica/
    url(r'classifica/$', views.classifica, name='classifica'),

    # /utenti/cerca/
    url(r'cerca/$', views.cerca_utenti, name='cerca_utenti'),

    # /check_username/?username=john
    url(r'check_username/$', views.check_username, name='check_username'),
]
