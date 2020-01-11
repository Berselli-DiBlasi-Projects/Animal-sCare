from django import forms
from .models import Annuncio, Servizio


class AnnuncioForm(forms.ModelForm):
    required_css_class = 'required'
    descrizione = forms.CharField(widget=forms.Textarea)
    scelta_animali = (('Cane', 'Cane'), ('Gatto', 'Gatto'), ('Coniglio', 'Coniglio'), ('Volatile', 'Volatile'),
                      ('Rettile', 'Rettile'), ('Altro', 'Altro'))
    pet = forms.ChoiceField(choices=scelta_animali)
    logo_annuncio = forms.ImageField()

    class Meta:
        model = Annuncio
        fields = ['titolo', 'sottotitolo', 'descrizione', 'data_inizio', 'data_fine',
                  'pet', 'pet_coins', 'logo_annuncio']


class ServizioForm(forms.ModelForm):
    class Meta:
        model = Servizio
        fields = ['passeggiate', 'pulizia_gabbia', 'ore_compagnia', 'cibo', 'accompagna_dal_vet']

