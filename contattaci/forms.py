from django import forms


class ContattaciForm(forms.Form):
    required_css_class = 'required'
    titolo = forms.CharField()
    messaggio = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['titolo', 'messaggio']
