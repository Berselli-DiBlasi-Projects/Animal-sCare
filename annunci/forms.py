from django import forms
from .models import Annuncio, Servizio


class AnnuncioForm(forms.ModelForm):
    required_css_class = 'required'
    descrizione = forms.CharField(widget=forms.Textarea)
    data_inizio = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    data_fine = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    scelta_animali = (('Cane', 'Cane'), ('Gatto', 'Gatto'), ('Coniglio', 'Coniglio'), ('Volatile', 'Volatile'),
                      ('Rettile', 'Rettile'), ('Altro', 'Altro'))
    pet = forms.ChoiceField(choices=scelta_animali)
    logo_annuncio = forms.ImageField(required=False)

    class Meta:
        model = Annuncio
        fields = ['titolo', 'sottotitolo', 'descrizione', 'data_inizio', 'data_fine',
                  'pet', 'pet_coins', 'logo_annuncio']


class ServizioForm(forms.ModelForm):
    class Meta:
        model = Servizio
        fields = ['passeggiate', 'pulizia_gabbia', 'ore_compagnia', 'cibo', 'accompagna_dal_vet']

