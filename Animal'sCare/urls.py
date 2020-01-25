from main import views as main_views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('main.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^annunci/', include('annunci.urls')),
    url(r'^contattaci/', include('contattaci.urls')),
    url(r'^utenti/', include('utenti.urls')),
    url(r'^recensioni/', include('recensioni.urls')),
    url('', include('social_django.urls', namespace='social')),
]

handler404 = main_views.handler404
handler500 = main_views.handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
