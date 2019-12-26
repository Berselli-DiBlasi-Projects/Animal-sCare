from django.contrib import admin
from .models import Annuncio, Servizio


class AnnuncioAdmin(admin.ModelAdmin):
    fields = ['annuncio_petsitter', 'user', 'user_accetta', 'logo_annuncio', 'titolo', 'sottotitolo', 'descrizione',
              'pet_coins', 'pet', 'data_inizio', 'data_fine']


admin.site.register(Annuncio, AnnuncioAdmin)
admin.site.register(Servizio)
