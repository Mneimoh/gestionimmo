from django import forms

class UserLoginForm(forms.Form):
    password = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=60)

