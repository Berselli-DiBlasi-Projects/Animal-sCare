from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import TestCase
from utenti.models import Profile
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user_normale = User.objects.create_user(username='normale', password='12345')
        self.profile = Profile.objects.get(user=self.user_normale)
        self.profile.indirizzo='Via Vivarelli'
        self.profile.citta='Modena'
        self.profile.provincia='Modena'
        self.profile.regione='Emilia Romagna'
        self.profile.latitudine=0
        self.profile.longitudine=0
        self.profile.telefono=3391234567
        self.profile.pet_coins=100
        self.profile.foto_profilo=None
        self.profile.pet_sitter=False
        self.profile.nome_pet='Ugo'
        self.profile.pet='Cane'
        self.profile.razza='Shihtzu'
        self.profile.eta=12
        self.profile.caratteristiche='Allergico a quasi tutto'
        self.profile.save()

    def test_foto_profilo_or_default(self):
        self.assertEquals(self.profile.foto_profilo_or_default(), static("/images/user_default.jpg"))

    def test_foto_pet_or_default(self):
        self.assertEquals(self.profile.foto_pet_or_default(), static("/images/pet_default.jpg"))
