from django.contrib.auth.models import User
from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    indirizzo = models.CharField(max_length=100)
    citta = models.CharField(max_length=50)
    provincia = models.CharField(max_length=2)
    regione = models.CharField(max_length=50)
    latitudine = models.FloatField(null=True, default=0, blank=True)
    longitudine = models.FloatField(null=True, default=0, blank=True)
    telefono = models.CharField(max_length=20)
    pet_coins = models.IntegerField(default=0)
    foto_profilo = models.FileField(null=True, default='', blank=True)

    pet_sitter = models.BooleanField(default=False)

    nome_pet = models.CharField(max_length=50, default="", null=True)
    pet = models.CharField(max_length=50, default="", null=True)
    razza = models.CharField(max_length=50, default="", null=True)
    eta = models.PositiveIntegerField(null=True)                   # età del pet
    caratteristiche = models.CharField(max_length=250, default="", null=True)
    foto_pet = models.FileField(null=True, default='', blank=True)

    descrizione = models.CharField(max_length=250, default="", null=True)
    hobby = models.CharField(max_length=100, default="", null=True)

    def __str__(self):
        return self.user.username

    def foto_profilo_or_default(self, default_path=static("/images/user_default.jpg")):
        if self.foto_profilo:
            return settings.MEDIA_URL + str(self.foto_profilo)
        return default_path

    def foto_pet_or_default(self, default_path=static("/images/pet_default.jpg")):
        if self.foto_pet:
            return settings.MEDIA_URL + str(self.foto_pet)
        return default_path

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
