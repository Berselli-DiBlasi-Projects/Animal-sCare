from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Annuncio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    user_accetta = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_accetta')

    annuncio_petsitter = models.BooleanField(default=True)     # Indica se l'annuncio è stato inserito da un petsitter
    titolo = models.CharField(max_length=100)
    sottotitolo = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=250)
    pet_coins = models.PositiveIntegerField(default=0)
    pet = models.CharField(max_length=50)
    data_inizio = models.DateTimeField(default=datetime.now)
    data_fine = models.DateTimeField(default=datetime.now)
    logo_annuncio = models.FileField(default=None)


class Servizio(models.Model):
    annuncio = models.ForeignKey(Annuncio, on_delete=models.CASCADE)
    passeggiate = models.BooleanField(default=False)
    pulizia_gabbia = models.BooleanField(default=False)
    ore_compagnia = models.BooleanField(default=False)
    cibo = models.BooleanField(default=False)
    accompagna_dal_vet = models.BooleanField(default=False)

