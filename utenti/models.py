from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.CharField(max_length=100)
    citta = models.CharField(max_length=50)
    provincia = models.CharField(max_length=2)
    regione = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    pet_coins = models.IntegerField(default=0)
    foto_profilo = models.FileField()

    pet_sitter = models.BooleanField(default=False)

    nome_pet = models.CharField(max_length=50, default="", null=True)
    pet = models.CharField(max_length=50, default="", null=True)
    razza = models.CharField(max_length=50, default="", null=True)
    eta = models.PositiveIntegerField(null=True)                   # età del pet
    caratteristiche = models.CharField(max_length=250, default="", null=True)
    foto_pet = models.FileField(default='media/pet_default.jpg')

    descrizione = models.CharField(max_length=250, default="", null=True)
    hobby = models.CharField(max_length=100, default="", null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
