from django.conf.urls import url
from . import views

app_name = 'recensioni'

urlpatterns = [

    # /recensioni/nuova/#user_recensito/
    url(r'nuova/(?P<oid>[0-9]+)/$', views.nuova_recensione, name='nuova_recensione'),

    # /recensioni/ricevute/@username/
    url(r'ricevute/(?P<username>\w+)/$', views.recensioni_ricevute, name='recensioni_ricevute'),
]
