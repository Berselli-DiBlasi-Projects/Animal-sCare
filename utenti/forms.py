from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(forms.ModelForm):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, label="Nome")
    last_name = forms.CharField(max_length=30, label="Cognome")
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    conferma_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'conferma_password', 'first_name', 'last_name', 'email')


class UtenteNormaleForm(forms.ModelForm):
    required_css_class = 'required'
    caratteristiche = forms.CharField(widget=forms.Textarea)
    scelta_animali = (('Cane', 'Cane'), ('Gatto', 'Gatto'), ('Coniglio', 'Coniglio'), ('Volatile', 'Volatile'),
                      ('Rettile', 'Rettile'), ('Altro', 'Altro'))
    pet = forms.ChoiceField(choices=scelta_animali)
    foto_profilo = forms.ImageField()
    foto_pet = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['indirizzo', 'citta', 'telefono', 'foto_profilo', 'nome_pet', 'pet', 'razza', 'eta',
                  'caratteristiche', 'foto_pet']


class UtentePetSitterForm(forms.ModelForm):
    required_css_class = 'required'
    descrizione = forms.CharField(widget=forms.Textarea)
    foto_profilo = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['indirizzo', 'citta', 'telefono', 'foto_profilo', 'descrizione', 'hobby']
