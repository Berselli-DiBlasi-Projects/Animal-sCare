from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import TestCase
from utenti.models import Profile
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user_normale = User.objects.create_user(username='normale', password='12345')
        self.profile = Profile.objects.create(
            user=self.user_normale,
            indirizzo='Via Vivarelli',
            citta='Modena',
            provincia='Modena',
            regione='Emilia Romagna',
            latitudine=0,
            longitudine=0,
            telefono=3391234567,
            pet_coins=100,
            foto_profilo=None,
            pet_sitter=False,
            nome_pet='Ugo',
            pet='Cane',
            razza='Shihtzu',
            eta=12,
            caratteristiche='Allergico a quasi tutto'
        )

    def test_foto_profilo_or_default(self):
        self.assertEquals(self.profile.foto_profilo_or_default(), static("/images/user_default.jpg"))

    def test_foto_pet_or_default(self):
        self.assertEquals(self.profile.foto_pet_or_default(), static("/images/pet_default.jpg"))
