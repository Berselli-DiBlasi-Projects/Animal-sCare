from django.conf.urls import url
from . import views

app_name = 'contattaci'

urlpatterns = [

    # /contattaci/
    url(r'^$', views.contattaci, name='contattaci'),
]