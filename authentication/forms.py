from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder": "Username"
        }
    ))
    password = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Password",
            "type": "password"
        }
    ))
