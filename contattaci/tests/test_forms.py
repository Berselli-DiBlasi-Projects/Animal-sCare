from django.test import TestCase
from contattaci.forms import ContattaciForm


class TestForms(TestCase):

    def test_contattaci_form_valid_data(self):
        form = ContattaciForm(data={
            'titolo': 'Un titolo',
            'messaggio': 'Un messaggio'
        })

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = ContattaciForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
