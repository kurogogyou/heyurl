from django import forms

class UrlForm(forms.Form):
    original_url = forms.CharField(label='Original URL', max_length=255)