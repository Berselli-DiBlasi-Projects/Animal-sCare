from django.test import TestCase
from annunci.forms import AnnuncioForm


class TestForms(TestCase):

    def test_annuncio_form_valid_data(self):
        form = AnnuncioForm(data={
            'titolo': 'Un titolo',
            'sottotitolo': 'Un sottotitolo',
            'descrizione': 'Una descrizione',
            'data_inizio': '15/08/2140 15:00',
            'data_fine': '16/08/2140 15:00',
            'pet': 'Cane',
            'pet_coins': 3
        })

        self.assertTrue(form.is_valid())

    def test_annuncio_form_no_data(self):
        form = AnnuncioForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)
