from django import forms
from .models import Annuncio, Servizio
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import magic
import re
MIME_TYPES = ['image/jpeg', 'image/png']


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

    def clean_titolo(self):
        # controllo titolo
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", self.cleaned_data['titolo']):
            raise ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(self.cleaned_data['titolo']) <= 95):
            raise ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['titolo']

    def clean_sottotitolo(self):
        # controllo sottotitolo
        if not re.match("^[A-Za-z0-9 ,.')èòàùì]+$", self.cleaned_data['sottotitolo']):
            raise ValidationError(_('Errore: il sottotitolo può contenere solo lettere, '
                                    'numeri, punti, virgole e spazi.'))
        if not (1 <= len(self.cleaned_data['sottotitolo']) <= 95):
            raise ValidationError(_('Errore: il sottotitolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return self.cleaned_data['sottotitolo']

    def clean_descrizione(self):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", self.cleaned_data['descrizione']):
            raise ValidationError(_('Errore: la descrizione può contenere solo lettere, '
                                    'numeri, punti, virgole e spazi.'))
        if not (1 <= len(self.cleaned_data['descrizione']) <= 245):
            raise ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 245 caratteri.'))
        return self.cleaned_data['descrizione']

    def clean_data_inizio(self):
        # controllo se data inizio < data_fine e se data_inizio e data_fine > adesso
        data_inizio = self.cleaned_data['data_inizio']
        if data_inizio < datetime.now():
            raise ValidationError(_('Errore: la data di inizio non può essere nel passato.'))
        return self.cleaned_data['data_inizio']

    def clean_data_fine(self):
        # controllo se data inizio < data_fine e se data_inizio e data_fine > adesso
        data_inizio = self.cleaned_data['data_inizio']
        data_fine = self.cleaned_data['data_fine']
        if data_inizio >= data_fine:
            raise ValidationError(_('Errore: la data di inizio deve avvenire prima della data di '
                                    'fine e non possono essere uguali.'))
        if data_fine < datetime.now():
            raise ValidationError(_('Errore: la data di fine non può essere nel passato.'))
        return self.cleaned_data['data_fine']

    def clean_pet_coins(self):
        # controllo pet_coins
        if not re.match("^[0-9]+$", str(self.cleaned_data['pet_coins'])):
            raise ValidationError(_('Errore: il campo pet coins può contenere solo numeri.'))
        if not (1 <= int(self.cleaned_data['pet_coins']) <= 100000):
            raise ValidationError(_('Errore: il valore in pet coins deve essere compreso tra 1 e 100000.'))
        return self.cleaned_data['pet_coins']

    def clean_logo_annuncio(self):
        files = self.files.get('logo_annuncio')
        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise forms.ValidationError(_("file non supportato."))
            return files
        return None


class ServizioForm(forms.ModelForm):
    class Meta:
        model = Servizio
        fields = ['passeggiate', 'pulizia_gabbia', 'ore_compagnia', 'cibo', 'accompagna_dal_vet']
