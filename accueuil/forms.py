from django.forms import ModelForm, fields, models
from main.models import Appointment

# class AppointmentForm(forms.Form):
#     nom = forms.CharField(max_length=30)
#     prenom = forms.CharField(max_length=30)
#     num_client = forms.CharField(max_length=10)
#     telephone = forms.CharField(max_length=15)
#     how_connu = forms.TextInput()
#     date_dappel = forms.DateField()
#     heure_dappel =  forms.TextInput()
#     article_dinteret = forms.TextInput()
#     date_redezvous = forms.DateTimeField()
#     heure_redezvous = forms.TimeField()

class AppointmentForms(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'