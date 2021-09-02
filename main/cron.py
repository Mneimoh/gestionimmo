from main.models import Societe,Facture
from datetime import datetime


def Greetings():
    new_societe = Societe(
        nom = "karlson",
        localisation = "Douala Cameroon",
        active = True,
        telephone = "654451039",
        ville = "Douala",
        pays = "Cameroon",
        code_postal = "100245",
        address = " Ange Raphael"
    )

    new_societe.save()
    
def updateFacture():
    current_date  = datetime.now().day
    current_month = datetime.now().month
    current_year  = datetime.now().year
    
    all_Facture  = Facture.objects.all()
    for Facture in all_Facture:




def UpdateFacture():
    pass