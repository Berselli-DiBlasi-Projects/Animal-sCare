from django import forms
from .models import Recensione


class RecensioneForm(forms.ModelForm):
    required_css_class = 'required'
    descrizione = forms.CharField(widget=forms.Textarea)
    voto_select = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    voto = forms.ChoiceField(choices=voto_select)

    class Meta:
        model = Recensione
        fields = ['titolo', 'descrizione', 'voto']
