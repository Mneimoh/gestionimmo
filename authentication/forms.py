from django import forms

class UserLoginForm(forms.Form):
<<<<<<< HEAD
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)
=======
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
>>>>>>> bcd0a8e9874204ea81ddce6332be2209e47585ba
