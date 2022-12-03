from django import forms

class ShareForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    comments = forms.CharField(max_length=500)
