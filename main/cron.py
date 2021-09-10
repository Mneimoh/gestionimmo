from main.models import Societe, Facture, Dossier
from datetime import datetime


def Greetings():
    new_societe = Societe(
        nom="karlson",
        localisation="Douala Cameroon",
        active=True,
        telephone="654451039",
        ville="Douala",
        pays="Cameroon",
        code_postal="100245",
        address=" Ange Raphael"
    )

    new_societe.save()


def updateFacture():
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    all_dossier = Dossier.objects.all()
    for dossier in all_dossier:
        end_date = dossier.facture.date
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        if end_year >= current_year:
            if end_month >= current_month:
                if end_day >= current_day:
                    dossier.statut = 'R'
                    dossier.save()
