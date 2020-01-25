from django.test import TestCase
from recensioni.forms import RecensioneForm


class TestForms(TestCase):

    def test_recensione_form_valid_data(self):
        form = RecensioneForm(data={
            'titolo': 'Recensione',
            'descrizione': 'Una descrizione',
            'voto': 5
        })

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = RecensioneForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
