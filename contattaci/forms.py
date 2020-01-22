from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ContattaciForm(forms.Form):
    required_css_class = 'required'
    titolo = forms.CharField()
    messaggio = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['titolo', 'messaggio']

    def clean_titolo(self):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", self.cleaned_data['titolo']):
            raise ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(self.cleaned_data['titolo']) <= 95):
            raise ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['titolo']

    def clean_messaggio(self):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", self.cleaned_data['messaggio']):
            raise ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(self.cleaned_data['messaggio']) <= 300):
            raise ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 300 caratteri.'))
        return self.cleaned_data['titolo']
