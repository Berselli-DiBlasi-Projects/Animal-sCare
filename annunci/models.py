from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

class Annuncio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    user_accetta = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_accetta')

    annuncio_petsitter = models.BooleanField(default=True)     # Indica se l'annuncio è stato inserito da un petsitter
    titolo = models.CharField(max_length=100)
    sottotitolo = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=250)
    pet_coins = models.PositiveIntegerField(default=0)
    pet = models.CharField(max_length=50)
    data_inizio = models.DateTimeField(default=timezone.now)
    data_fine = models.DateTimeField(default=timezone.now)
    logo_annuncio = models.FileField(null=True, default='', blank=True)

    def logo_annuncio_or_default(self, default_path=static("/images/annuncio_default.jpg")):
        if self.logo_annuncio:
            return settings.MEDIA_URL + str(self.logo_annuncio)
        return default_path

    class Meta:
        verbose_name = 'Annuncio'
        verbose_name_plural = "Annunci"


class Servizio(models.Model):
    annuncio = models.ForeignKey(Annuncio, on_delete=models.CASCADE)
    passeggiate = models.BooleanField(default=False)
    pulizia_gabbia = models.BooleanField(default=False)
    ore_compagnia = models.BooleanField(default=False)
    cibo = models.BooleanField(default=False)
    accompagna_dal_vet = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Servizio'
        verbose_name_plural = "Servizi"

