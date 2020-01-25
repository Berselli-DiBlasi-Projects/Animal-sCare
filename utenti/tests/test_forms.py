from django.test import TestCase
from utenti.forms import UserForm, UtenteNormaleForm, UtentePetSitterForm


class TestForms(TestCase):

    def test_user_form_valid_data(self):
        form = UserForm(data={
            'username': 'mariorossi',
            'first_name': 'Mario',
            'last_name': 'Rossi',
            'email': 'mario.rossi@gmail.com',
            'password': 'pass123',
            'conferma_password': 'pass123'
        }, oauth_user=0)

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = UserForm(data={}, oauth_user=0)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_utente_normale_form_valid_data(self):
        form = UtenteNormaleForm(data={
            'indirizzo': 'Via Vivarelli',
            'citta': 'Modena',
            'provincia': 'MO',
            'regione': 'Emilia-Romagna',
            'telefono': 3391234556,
            'nome_pet': 'Ugo',
            'pet': 'Cane',
            'razza': 'Shihtzu',
            'eta': 12,
            'caratteristiche': 'Allergico a quasi tutto'
        })

        self.assertTrue(form.is_valid())

    def test_utente_normale_form_no_data(self):
        form = UtenteNormaleForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 10)

    def test_utente_petsitter_form_valid_data(self):
        form = UtentePetSitterForm(data={
            'indirizzo': 'Via Vivarelli',
            'citta': 'Modena',
            'provincia': 'MO',
            'regione': 'Emilia-Romagna',
            'telefono': 3391234556,
            'descrizione': 'ABC',
            'hobby': 'Chitarra'
        })

        self.assertTrue(form.is_valid())

    def test_utente_petsitter_form_no_data(self):
        form = UtentePetSitterForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)
