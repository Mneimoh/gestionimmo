from django.db import connections
from django.http import response
import societe
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from accueuil.views import appointment
from django.db.models.expressions import F
from django.forms.widgets import DateInput
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from .forms import ClientForms, PlaceForm, EmploiForm, EndettementForm
from main.models import Client, Facture, Place, Emploi, Endettement, CompteEndettement, PretEndettement, Dossier, Cosignataire, Article, Appointment, Credit, Societe
from django.core.mail import send_mail
import uuid
import smtplib
import random

# IMPORTS FOR SEARCH
from django.db.models import Q
from transac.serializers import DossierSerializer

# IMPORTS FOR API CALL
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import for the pdf creator
from django.http import FileResponse
import io
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from textwrap import wrap

# Declaring Global Variables.
section = 'transac'
errors = ''
globvar = 0
proprietaire = False
parents = False
charges = False
compte = False
nom_banque = None
type_compte = None
article_interet = None
client_interet = None
clientData = None
currentDossier = None
clientForm = ClientForms()
placeForm = PlaceForm()
emploiForm = EmploiForm()
endettementForm = EndettementForm()


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def index(request, nom):
    if(request.user.poste == section):
        appointment_id = int(nom)
        client = Appointment.objects.get(pk=appointment_id)
        print(client)
        articles = Article.objects.all()
        all_clients = Client.objects.filter(
            societe=request.user.societe, cosigner=None)
        return render(request, 'transac/tcompte.html', {'title': 'Espace ouverture compte', 'clientForm': ClientForms, 'article_interet': articles, 'client': client, 'clients': all_clients})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def prequalifList(request):
    if(request.user.poste == section):
        all_prequalifier = Appointment.objects.filter(
            societe=request.user.societe).filter(status="PQ")

        return render(request, 'transac/tprequalifier.html', {'title': 'Liste Prequalifier', "all_prequalifiers": all_prequalifier})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def registerAccount(request, table=None, type=None):

    if(request.method == 'POST' and request.user.poste == section):
        global globvar, clientForm, emploiForm, placeForm, endettementForm, proprietaire, parents, charges, compte, nom_banque, type_compte, clientData, article_interet, client_interet

        if globvar >= 4:
            globvar = 0
        data_type = request.path.split('/')[-1]
        data_type = table

        if (data_type == 'client'):
            globvar = globvar + 1
            clientForm = ClientForms(request.POST)
            if type == "True":
                article_interet = request.POST['article_interet']
            else:
                client_interet = request.POST['client_interet']

        if (data_type == 'emploi'):
            globvar = globvar + 1
            emploiForm = EmploiForm(request.POST)

        if (data_type == 'place'):
            globvar = globvar + 1
            placeForm = PlaceForm(request.POST)
            proprietaire = request.POST['proprietaire']
            parents = request.POST['parents']

        if (data_type == 'endettement'):
            globvar = globvar + 1
            nom_banque = request.POST['nom_banque']
            charges = request.POST['charge']
            compte = request.POST['compte']
            # type_compte = request.POST['type_compte']
            endettementForm = EndettementForm(request.POST)
            type_compte = request.POST.get('type_compte', None)

        print(globvar)
        if(globvar == 4):
            client_check = clientForm.is_valid()
            emploi_check = emploiForm.is_valid()
            place_check = placeForm.is_valid()
            dette_check = endettementForm.is_valid()

            if client_check and place_check and emploi_check and dette_check:

                new_endettement = Endettement(
                    phone_emploi=endettementForm.cleaned_data.get(
                        'phone_emploi'),
                    nom_responsable=endettementForm.cleaned_data.get(
                        'nom_responsable'),
                    saisi=endettementForm.cleaned_data.get('saisi'),
                    faillite=endettementForm.cleaned_data.get('faillite'),
                    charge=charges,
                    charge_sum=endettementForm.cleaned_data.get(
                        'phone_emploi'),
                )

                new_endettement.save()

                new_emploi = Emploi(
                    denomination=emploiForm.cleaned_data.get('denomination'),
                    nom_societe=emploiForm.cleaned_data.get('nom_societe'),
                    adresse=emploiForm.cleaned_data.get('adresse'),
                    ville=emploiForm.cleaned_data.get('ville'),
                    pays=emploiForm.cleaned_data.get('pays'),
                    salaire_m=emploiForm.cleaned_data.get('salaire_m'),
                    anciennete=emploiForm.cleaned_data.get('anciennete'),
                    poste_actu=emploiForm.cleaned_data.get('poste_actu'),
                    autre_revenu=emploiForm.cleaned_data.get('autre_revenu'),
                    autre_rev_sum=emploiForm.cleaned_data.get(
                        'autre_revenu_sum'),
                    ancien_denomination=emploiForm.cleaned_data.get(
                        'ancien_denomination'),
                    ancien_nom_societe=emploiForm.cleaned_data.get(
                        'ancien_nom_societe'),
                    ancien_adresse=emploiForm.cleaned_data.get(
                        'ancien_adresse'),
                    ancien_ville=emploiForm.cleaned_data.get('ancien_ville'),
                    ancien_code_postal=emploiForm.cleaned_data.get(
                        'ancien_code_postal'),
                    ancien_pays=emploiForm.cleaned_data.get('ancien_pays'),
                    ancien_salaire_m=emploiForm.cleaned_data.get(
                        'ancien_salaire_m'),
                    ancien_anciennete=emploiForm.cleaned_data.get(
                        'ancien_anciennete'),

                )

                new_emploi.save()

                new_place = Place(
                    adresse=placeForm.cleaned_data.get('adresse'),
                    ancienne_address=placeForm.cleaned_data.get(
                        'ancienne_address'),
                    ville=placeForm.cleaned_data.get('ville'),
                    ancienne_ville=placeForm.cleaned_data.get(
                        'ancienne_ville'),
                    pays=placeForm.cleaned_data.get('pays'),
                    ancienne_pays=placeForm.cleaned_data.get('ancienne_pays'),
                    loyer=placeForm.cleaned_data.get('loyer'),
                    ancienne_loyer=placeForm.cleaned_data.get(
                        'ancienne_loyer'),
                    code_postal=placeForm.cleaned_data.get('code_postal'),
                    ancienne_code_postal=placeForm.cleaned_data.get(
                        'ancienne_code_postal'),
                    anciennete=placeForm.cleaned_data.get('anciennete'),
                    ancienne_anciennete=placeForm.cleaned_data.get(
                        'ancienne_anciennete'),
                )

                new_place.save()

                # Register either the client or the cosigner
                print(type == "True")
                if type == "True":
                    # Storing a new Client
                    new_client = Client(
                        societe=request.user.societe,
                        User=request.user,
                        nom=clientForm.cleaned_data.get('nom'),
                        prenom=clientForm.cleaned_data.get('prenom'),
                        email=clientForm.cleaned_data.get('email'),
                        phone_1=clientForm.cleaned_data.get('phone_1'),
                        phone_2=clientForm.cleaned_data.get('phone_2'),
                        how_connu=clientForm.cleaned_data.get('how_connu'),
                        date_naissance=clientForm.cleaned_data.get(
                            'date_naissance'),
                        ville_naissance=clientForm.cleaned_data.get(
                            'ville_naissance'),
                        type_piece_id=clientForm.cleaned_data.get(
                            'type_piece_id'),
                        numero_piece_id=clientForm.cleaned_data.get(
                            'numero_piece_id'),
                        pays_naissance=placeForm.cleaned_data.get('pays'),
                        parents=bool(parents),
                        proprietaire=bool(proprietaire),
                        place=new_place,
                        emploi=new_emploi,
                        endettement=new_endettement,
                        uid=int(random.random()*1000000000)
                    )
                    print(
                        '******************saving new client***********************************')
                    new_client.save()
                    print(
                        '******************saving new client***********************************')

                    clientData = new_client
                    return HttpResponse('client_created')

                else:
                    # Saving and assigning a clients Cosigner
                    new_cosigner = Cosignataire(
                        societe=request.user.societe,
                        User=request.user,
                        nom=clientForm.cleaned_data.get('nom'),
                        prenom=clientForm.cleaned_data.get('prenom'),
                        email=clientForm.cleaned_data.get('email'),
                        phone_1=clientForm.cleaned_data.get('phone_1'),
                        phone_2=clientForm.cleaned_data.get('phone_2'),
                        how_connu=clientForm.cleaned_data.get('how_connu'),
                        date_naissance=clientForm.cleaned_data.get(
                            'date_naissance'),
                        ville_naissance=clientForm.cleaned_data.get(
                            'ville_naissance'),
                        type_piece_id=clientForm.cleaned_data.get(
                            'type_piece_id'),
                        numero_piece_id=clientForm.cleaned_data.get(
                            'numero_piece_id'),
                        pays_naissance=placeForm.cleaned_data.get('pays'),
                        parents=bool(parents),
                        proprietaire=bool(proprietaire),
                        place=new_place,
                        emploi=new_emploi,
                        endettement=new_endettement,
                    )
                    new_cosigner.save()

                    print('******** you are here ***********')
                    client = Client.objects.get(pk=int(client_interet))
                    client.cosigner = new_cosigner
                    client.save()

                    appointment_to_delete = Appointment.objects.filter(
                        nom=client.nom, prenom=client.prenom)[0]

                    print(
                        '************************* apointment to delete  *************************')
                    print(appointment_to_delete)
                    print(
                        '************************* apointment to delete  *************************')

                    article_interet = appointment_to_delete.article_dinteret

                    # Creating the Clients Dossier

                    article_interet = article_interet
                    article = Article.objects.filter(
                        nom=article_interet)

                    if article:
                        article = article[0]
                        print(
                            '##################### article found #####################')
                        print(article)
                        print(
                            '##################### article found #####################')
                        # Creating Client forms
                        new_credit = Credit(
                            article=article,
                            societe=request.user.societe,
                            somme_payee=0.0
                        )

                        new_credit.save()

                        # Creating the clients facture after applied
                        new_facture = Facture(
                            article=article,
                            User_editeur=request.user,
                            statut="OM",
                            num_facture="",
                            somme=article.frais_montage
                        )
                        new_facture.save()

                        new_dossier = Dossier(
                            societe=request.user.societe,
                            User=request.user,
                            client=client,
                            credit=new_credit,
                            article_interet=article,
                            facture=new_facture,
                            statut='OM',
                            coeff_recouv=0,
                            pin=0,
                            verifie=False,
                            uid=int(random.random()*1000000000)
                        )

                        print(
                            '/////////////////////////////saving client/////////////////////////////////')
                        new_dossier.save()
                        print(
                            '//////////////////// /////////saving client/////////////////////////////////')

                        currentDossier = new_dossier
                        appointment_to_delete.status = 'DONE'
                        appointment_to_delete.save()
                        return HttpResponse('validated')

                new_compte_endettement = CompteEndettement(
                    endettement=new_endettement,
                    nom_banque=nom_banque,
                    type_compte=type_compte,
                    compte=compte,
                    nom_compte=endettementForm.cleaned_data.get('nom_compte'),
                )

                new_compte_endettement.save()

                new_preendettement = PretEndettement(
                    endettement=new_endettement,
                    nom_banque=nom_banque,
                    type_pret=endettementForm.cleaned_data.get('type_pret'),
                    reste=endettementForm.cleaned_data.get('reste'),
                    mensualite=endettementForm.cleaned_data.get('mensualite'),
                    nom_banque_1=endettementForm.cleaned_data.get(
                        'nom_banque_1'),
                    type_pret_1=endettementForm.cleaned_data.get(
                        'type_pret_1'),
                    reste_1=endettementForm.cleaned_data.get('reste_1'),
                    mensualite_1=endettementForm.cleaned_data.get(
                        'mensualite_1'),
                    nom_banque_2=endettementForm.cleaned_data.get(
                        'nom_banque_2'),
                    type_pret_2=endettementForm.cleaned_data.get(
                        'type_pret_2'),
                    reste_2=endettementForm.cleaned_data.get('reste_2'),
                    mensualite_2=endettementForm.cleaned_data.get(
                        'mensualite_2'),
                    date=endettementForm.cleaned_data.get('date'),

                )

                # new_preendettement.save()
                # return HttpResponse('success')
            else:
                errors = f'Info Perso Client <br />{clientForm.errors}<br />Info Address Client <br />{placeForm.errors}<br />Info Emploi <br /> {emploiForm.errors} <br /> Info Endettement <br /> {endettementForm.errors} <br /> '

                return HttpResponse(errors)

        return HttpResponse('')


@login_required
def save_credit(request, dossier):
    matching_dossier = Dossier.objects.filter(uid=int(dossier))
    if matching_dossier:
        client_dossier = matching_dossier[0]
        credit_pk = client_dossier.credit.pk
        credit = Credit.objects.get(pk=credit_pk)
        credit.accompte = request.POST['accompte']
        credit.taux = request.POST['taux']
        credit.total = request.POST['total']
        credit.frais_dossier = request.POST['frais_dossier']
        credit.autre_frais = request.POST['frais_autre']
        credit.montant = request.POST['paiement_mensuel']
        credit.date_fin = request.POST['date_fin']

        credit.save()

        return HttpResponse('hello')


@login_required
def sendMail(request, id):
    if(request.method == 'POST' and request.user.poste == section):
        print(request.path)
        print(request.POST)
        appointed_user = Appointment.objects.get(pk=int(id))
        print(appointed_user)
        name = appointed_user.nom
        prenom = appointed_user.prenom
        client = Client.objects.filter(nom=name, prenom=prenom)
        print('********** client **************')
        print(client[0])
        print('********** client **************')
        cosigner_email = client[0].cosigner.email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('karlsedoide@gmail.com', '40sedoide40')

        subject = "Greetings From GestionImmo"
        # body = f"This is to notify you that our client of name {request.POST['crediteur_name']} of the town {request.POST['crediteur_adresse']} with POSTal code of  {request.POST['crediteur_code_postal']}  took a loan from our company called {request.user.societe}"
        body = f"""
        Nous vous informons que Monsieur/Madamme {request.POST['debiteur_name']}, demeurant au {request.POST['debiteur_adresse']}, vous a ajoute en cosignataire pour la  souscription d'un credit aupres de notre organisme {request.user.societe}
        Attention, on vous demande de vous porter garant pour un pret. Reflechissez tres bien avant de vous engager. Si l'emprunteur ne paye pas sa dette, vous serez dans l'obligation de le faire a sa place. Soyez sur d'avoir les moyens de le faire, et que vous avez envie de prendre cette responsabilite.
        Vous pourriez etre obliger de payer la totalite de la dette si l'emprunteur ne paye pas. Vous pourriez aussi payer des dommages et interets plus frais de procedures, et les montants changeraient en consequence.
        Nous pourrions recuperer nos paiements a votre niveau sans pour autant essayer de recuperer au niveau de l'emprunteur. Nous pourrions utiliser contre vous les memes methodes de recouvrement que nous utiliserions contre l'emprunteur, comme une poursuite judiciaire, coupures de vos salaires a la source, etc....
        Cette notification n'est pas le contrat qui nous lie.    

        La direction {request.user.societe}         

        """
        msg = f"{subject}\n\n{body}"
        server.sendmail(
            'karlsedoide@gmail.com',
            cosigner_email,
            msg
        )
        print('----- Email Sent Successfully -----')

        server.quit()
        return HttpResponse('success')

    else:
        pass


@login_required
def getPdf(request, name, dossier):
    dossier_uid = int(dossier)
    if dossier_uid < 1000000:
        dossier = Dossier.objects.get(id=dossier_uid)
    else:
        dossier = Dossier.objects.get(uid=dossier_uid)
    print(dossier)
    print(name)
    template_path = None
    if name == 'facture':
        template_path = 'transac/vente_facture.html'
    if name == "engagement":
        template_path = 'transac/engagement.html'
    if name == "recapitulatif":
        template_path = 'transac/recapitulatif.html'
    if name == "ppe_imp":
        template_path = 'transac/ppe_imp.html'
    if name == "ppr_imp":
        template_path = 'transac/ppr_imp.html'
    if name == "pvi_imp":
        template_path = "transac/pvi_imp.html"
    if name == "ct_imp":
        template_path = "transac/ct_imp.html"
    if name == "bal_imp":
        template_path = "transac/bal_imp.html"
    if name == "ppe_imp":
        template_path = "transac/ppe_imp.html"
    if name == "authorise":
        template_path = "transac/authorise.html"

    context = {'dossier': dossier}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def vente(request):
    global currentDossier
    dossier_uid = None
    if(request.user.poste == section):
        if request.method == 'POST':
            print(request.POST)
            if request.POST['article_interet'] == "No de dossier":
                dossier_uid = int(request.POST['dossier_id'])
                currentDossier = Dossier.objects.filter(uid=dossier_uid)[0]
            if request.POST['article_interet'] == "Telephone":
                phone = int(request.POST['dossier_id'])
                currentDossier = Dossier.objects.filter(
                    client__phone_1=phone)[0]
            if request.POST['article_interet'] == "Nom":
                name = request.POST['dossier_id']
                currentDossier = Dossier.objects.filter(client__nom=name)[0]

            return render(request, 'transac/tvente.html', {'title': 'Espace vente', 'client': clientData, 'dossier': currentDossier})

        return render(request, 'transac/tvente.html', {'title': 'Espace vente', 'client': clientData, 'dossier': currentDossier})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def venteSearch(request):
    if(request.user.poste == section):
        print('*************** welcome ********************')
        print('hemmorphine')
        print('*************** welcome ********************')
        if request.method == 'POST':
            print(request.POST)
            # *************************************  Testing  ******************************************
            uid = request.POST['dossier_id']
            phone_1 = request.POST['dossier_id']
            nom = request.POST['dossier_id']
            prenom = request.POST['dossier_id']
            statut = request.POST['dossier_id']
            dernier_appel = request.POST['dossier_id']
            coeff_recouv = request.POST['dossier_id']
            appele_recouvre = request.POST['dossier_id']

            # FOR SEARCH FIELD BELLOW
            search_table = request.POST['dossier_id']
            print('GOT HERE IN GET CAISSE')

            caisse_info = Dossier.objects.filter(
                societe__nom=request.user.societe)

            if search_table:
                lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
                    uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

                caisse_info = caisse_info.filter(lookups).distinct()

                # if uid:
                #     caisse_info = caisse_info.all().order_by('client__uid')
                # if phone_1:
                #     caisse_info = caisse_info.all().order_by('client__phone_1')
                # if nom:
                #     caisse_info = caisse_info.all().order_by('client__nom')
                # if prenom:
                #     caisse_info = caisse_info.all().order_by('client__prenom')
                # if statut:
                #     caisse_info = caisse_info.all().order_by('statut')
                # if dernier_appel:
                #     caisse_info = caisse_info.all().order_by('dernier_appel')
                # if coeff_recouv:
                #     caisse_info = caisse_info.all().order_by('coeff_recouv')
                # if appele_recouvre:
                #     caisse_info = caisse_info.all().order_by('appele_recouvre')

                print('****************** just random spot *********************')
                dossier = caisse_info[0].uid
                currentDossier = Dossier.objects.get(uid=dossier)
                print(currentDossier)
                print(currentDossier.client)
                print('****************** just random spot *********************')

                return render(request, 'transac/tvente.html', {'title': 'Espace vente', 'client': currentDossier.client, 'dossier': currentDossier})


@login_required
def venteUpdates(request, _type, dossier, article):
    new_facture = None

    if(request.method == "GET"):
        if _type == "mutation":
            interested_article = Article.objects.get(pk=int(article))
            print('********************* mutated **********************')
            print(interested_article)
            print('********************* mutated **********************')
            dossier_uid = int(dossier)
            dossier = Dossier.objects.filter(uid=dossier_uid)[0]
            currentDossier = Dossier.objects.get(pk=dossier.pk)
            currentDossier.article_interet = interested_article
            currentDossier.save()
            return render(request, 'transac/tvente.html', {'title': 'Espace vente', 'client': clientData, 'dossier': currentDossier})

        if _type == "restructure":
            dossier_uid = int(dossier)
            dossier = Dossier.objects.filter(uid=dossier_uid)[0]
            currentDossier = Dossier.objects.get(pk=dossier.pk)
            return render(request, 'transac/tvente.html', {'title': 'Espace vente', 'client': clientData, 'dossier': currentDossier})

    if(request.method == "POST"):

        if _type == "mutation":
            print('************************************************')
            print('creating mutation facture')
            print('************************************************')
            # Creating the clients facture after applied
            dossier_uid = int(dossier)
            dossier = Dossier.objects.filter(uid=dossier_uid)[0]
            currentDossier = Dossier.objects.get(pk=dossier.pk)
            new_facture = Facture(
                article=currentDossier.article_interet,
                User_editeur=request.user,
                statut="MT",
                num_facture="",
                somme=15000
            )

            credit_pk = currentDossier.credit.pk
            credit = Credit.objects.get(pk=credit_pk)
            credit.accompte = request.POST['accompte']
            credit.taux = request.POST['taux']
            credit.total = int(request.POST['total']) - int(credit.somme_payee)
            credit.frais_dossier = request.POST['frais_dossier']
            credit.autre_frais = request.POST['frais_autre']
            credit.montant = request.POST['paiement_mensuel']
            credit.date_fin = request.POST['date_fin']
            credit.article = currentDossier.article_interet
            new_facture.save()
            credit.save()
            currentDossier.statut = "MT"
            currentDossier.facture = new_facture
            currentDossier.credit = credit
            currentDossier.save()
            return HttpResponse('success')

        if _type == "restructure":
            print('***********************************************')
            print('creating restructure factore')
            print('***********************************************')
            # Creating the clients facture after applied
            dossier_uid = int(dossier)
            dossier = Dossier.objects.filter(uid=dossier_uid)[0]
            currentDossier = Dossier.objects.get(pk=dossier.pk)
            print(currentDossier)

            new_facture = Facture(
                article=currentDossier.article_interet,
                User_editeur=request.user,
                statut="RT",
                num_facture="",
                somme=15000
            )
            new_facture.save()
            credit_pk = currentDossier.credit.pk
            credit = Credit.objects.get(pk=credit_pk)
            credit.accompte = request.POST['accompte']
            credit.taux = request.POST['taux']
            credit.total = int(request.POST['total']) - int(credit.somme_payee)
            credit.frais_dossier = request.POST['frais_dossier']
            credit.autre_frais = request.POST['frais_autre']
            credit.montant = request.POST['paiement_mensuel']
            credit.date_fin = request.POST['date_fin']
            credit.article = currentDossier.article_interet
            new_facture.save()
            credit.save()
            currentDossier.facture = new_facture
            currentDossier.save()


@login_required
def creditFacture(request, dossier):
    matching_dossier = Dossier.objects.filter(uid=int(dossier))
    if matching_dossier:
        client_dossier = matching_dossier[0]
        credit_pk = client_dossier.credit.pk
        credit = Credit.objects.get(pk=credit_pk)
        credit.accompte = request.POST['accompte']
        credit.taux = request.POST['taux']
        credit.somme_payee = request.POST['total']
        credit.frais_dossier = request.POST['frais_dossier']
        credit.autre_frais = request.POST['frais_autre']
        credit.montant = request.POST['paiement_mensuel']
        credit.date_fin = request.POST['date_fin']

        credit.save()

        new_facture = Facture(

        )


@login_required
def penalties(request):
    if(request.user.poste == section):

        lookup = Q(facture__penalty_status=True) | Q(statut='P1')
        all_info = Dossier.objects.filter(lookup)

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(lookup)
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/tpenalties.html', {'title': 'Pénalités', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def payments(request):
    if(request.user.poste == section):
        filterby = Q(statut="PM1")  # | Q(statut="A")
        all_info = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(filterby)

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(filterby)
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/tpaiement.html', {'title': 'Paiements', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def mutations(request):
    if(request.user.poste == section):

        all_info = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='A')
        all_articles = Article.objects.filter(societe=request.user.societe)

        print('******* mutation societes  ********')
        print(all_articles)
        print('***********************************')
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='A')
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/tmutations.html', {'title': 'Mutations', 'page_list': page_list, 'page': page, "all_dossier": all_info, 'all_articles': all_articles})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def restructure(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='A')

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='A')
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/trestructurations.html', {'title': 'Restructurations', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def plan(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='FN')

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='FN')
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/tpml.html', {'title': 'Plan de masse local', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


# @login_required
def dossiers_credit(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(societe__nom=request.user.societe).filter(
            statut='A').exclude(statut='OM')

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(societe__nom=request.user.societe).filter(
            statut='A').exclude(statut='OM')
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'transac/tdc.html', {'title': 'Dossiers crédits (DC)', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def dossiers(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(societe__nom=request.user.societe).filter(
            article_interet__type_article='TERRAIN')

        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(societe__nom=request.user.societe).filter(
            article_interet__type_article='TERRAIN')
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range
        return render(request, 'transac/tdcpt.html', {'title': 'Dossiers crédits propriétaires terriens (DCPT)', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


# ENDPOINTS FOR PENALITE BELLOW

@login_required
@api_view(['GET'])
def paginate_penalite(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1
    lookup = Q(statut="PN") | Q(statut='PN1')
    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        lookup)[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_penalite(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    lookup = Q(statut="PN") | Q(statut='PN1')
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(lookup)

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


@login_required
@api_view(['GET'])
def paginate_paiement(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1
    lookup = Q(statut="PM1") | Q(statut="A")
    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        lookup)[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_paiement(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    lookup = Q(statut="PM1") | Q(statut="A")
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(lookup)

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# ENDPOINTS FOR MUTATIONS BELLOW

@login_required
@api_view(['GET'])
def paginate_mutations(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    lookup = Q(statut='MT') | Q(statut='A')
    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        lookup)[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_mutations(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    lookup = Q(statut='MT') | Q(statut='A')
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(lookup)

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# ENDPOINTS FOR RESTRUCTURATIONS BELLOW

@login_required
@api_view(['GET'])
def paginate_restructurations(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1
    lookup = Q(statut='RT') | Q(statut='A')
    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        lookup)[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_restructurations(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    lookup = Q(statut='RT') | Q(statut='A')
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(lookup)

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# ENDPOINTS FOR CPML BELLOW

@login_required
@api_view(['GET'])
def paginate_tpml(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        statut='FN')[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_tpml(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(statut='FN')

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# ENDPOINTS FOR TDCPT BELLOW

@login_required
@api_view(['GET'])
def paginate_tdcpt(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        statut='TERRAIN')[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_tdcpt(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(statut='TERRAIN')

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# ENDPOINTS FOR TDC BELLOW

@login_required
@api_view(['GET'])
def paginate_tdc(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe).filter(
        statut='A')[starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_tdc(request):
    uid = request.query_params.get('uid', None)
    phone_1 = request.query_params.get('phone_1', None)
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    statut = request.query_params.get('statut', None)
    dernier_appel = request.query_params.get('dernier_appel', None)
    coeff_recouv = request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)

    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.filter(
        societe__nom=request.user.societe).filter(statut='A')

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(
            uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)

        caisse_info = caisse_info.filter(lookups).distinct()

    if uid:
        caisse_info = caisse_info.all().order_by('client__uid')
    if phone_1:
        caisse_info = caisse_info.all().order_by('client__phone_1')
    if nom:
        caisse_info = caisse_info.all().order_by('client__nom')
    if prenom:
        caisse_info = caisse_info.all().order_by('client__prenom')
    if statut:
        caisse_info = caisse_info.all().order_by('statut')
    if dernier_appel:
        caisse_info = caisse_info.all().order_by('dernier_appel')
    if coeff_recouv:
        caisse_info = caisse_info.all().order_by('coeff_recouv')
    if appele_recouvre:
        caisse_info = caisse_info.all().order_by('appele_recouvre')

    if caisse_info:
        serialized = DossierSerializer(caisse_info, many=True)
        return Response(serialized.data)
    else:
        return Response({})


# BELLOW ARE API CALL METHODS FOR THE 3 BUTTONS
@login_required
@api_view(['GET'])
def get_facture(request):
    id = request.query_params.get('id', None)
    # lookup = Q(uid=id)
    dossier = Dossier.objects.filter(uid=id)

    serialized = DossierSerializer(dossier, many=True)
    print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data[0])


# PAY FACTURE BUTTON FOR OM
@login_required
@api_view(['POST'])
def pay_facture(request):
    # id = request.query_params.get('id',None)
    id = request.POST.get('id', None)
    status = request.POST.get('status', None)
    dossier = Dossier.objects.get(pk=id)
    print('###################################')
    print(dossier)
    print('---  updating payment mensuel   ---')
    print('###################################')
    facture = Facture.objects.get(pk=dossier.facture.id)
    # dossier

    # GENERATE FACTURE

    if(dossier.statut == 'PM1'):
        print('********confirming pay*********')
        dossier.statut = status
        if dossier.credit.somme_payee >= dossier.credit.total:
            dossier.statut = 'FN'
        dossier.save()

    print('INFO BELLOW')
    print(facture)
    print(id)
    print(status)

    return Response({})


# SET PERCENT FOR FACTURE
@login_required
@api_view(['POST'])
def set_facture_penalty(request):
    # id = request.query_params.get('id',None)
    id = request.POST.get('id', None)
    type_of_amount = request.POST.get('type', None)
    value = request.POST.get('value', None)

    facture = Facture.objects.get(pk=id)

    if(type_of_amount == 'PERCENT'):
        # GET FACTURE AND CALCULATE PERCENT
        sum = int(facture.somme) * int(value) / 100
        print('#####SUM BELLOW#########')
        print(sum)
        facture.penalty_somme = sum
        facture.penalty_status = True
        facture.save()
    else:
        # GET FACTURE AND SUM AMOUNT
        sum = int(facture.somme) + int(value)
        print('#####SUM BELLOW#########')
        print(sum)
        facture.penalty_somme = sum
        facture.penalty_status = True
        facture.save()

    # facture = Facture.objects.get(pk=dossier.id)
    # dossier

    # GENERATE FACTURE

    # print('INFO BELLOW')
    # print(id)
    # print(status)

    return Response({})
