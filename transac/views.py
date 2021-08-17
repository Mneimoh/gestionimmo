from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.expressions import F
from django.forms.widgets import DateInput
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users
from .forms import ClientForms,PlaceForm,EmploiForm,EndettementForm
from main.models import Client, Facture,Place,Emploi,Endettement,CompteEndettement,PretEndettement, Dossier, Cosignataire,Article, Appointment, Credit, Societe     
from django.core.mail import send_mail
import uuid
import random

# IMPORTS FOR SEARCH
from django.db.models import  Q
from transac.serializers import DossierSerializer

# IMPORTS FOR API CALL
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import for the pdf creator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
from reportlab.lib.pagesizes import letter
from textwrap import wrap

# Declaring Global Variables.
section           = 'transac'
errors            = ''
globvar           = 0
proprietaire      = False
parents           = False
charges           = False
compte            = False
nom_banque        = None
type_compte       = None
article_interet   = None
client_interet    = None
clientData        = None
currentDossier    = None
clientForm        = ClientForms()
placeForm         = PlaceForm()
emploiForm        = EmploiForm()
endettementForm   = EndettementForm()



@login_required
def index(request,nom):
      if(request.user.poste == section): 
            fnom   = nom.split('-')[0]
            prenom  = nom.split('-')[1]
            # prenom  = ' '.join(prenom)
            print(fnom)
            print(prenom)
            client = Appointment.objects.filter(nom=fnom)
            if client:
                  client = client[0]
            articles = Article.objects.all()
            all_clients = Client.objects.filter(societe = request.user.societe, cosigner = None)
            print('##########ALL CLIENTS BELLOW##########')
            print(all_clients)
            return render(request, 'transac/tcompte.html', { 'title': 'Espace ouverture compte','clientForm':ClientForms,'article_interet':articles, 'client': client, 'clients':all_clients})
      else:
            return redirect(f"/login?next=/{section}/")


@login_required
def prequalifList(request):
      if(request.user.poste == section):  
            all_prequalifier = Appointment.objects.filter(status="PQ")
            return render(request, 'transac/tprequalifier.html', { 'title': 'Liste Prequalifier', "all_prequalifiers":all_prequalifier})
      else:
            return redirect(f"/login?next=/{section}/")


@login_required
def registerAccount(request,table=None,type=None):

      if(request.method == 'POST' and request.user.poste == section):
            global globvar,clientForm,emploiForm,placeForm,endettementForm,proprietaire,parents,charges,compte,nom_banque,type_compte,clientData, article_interet,client_interet
            
            
            if globvar>=4:
                  globvar = 0
            data_type = request.path.split('/')[-1]          
            data_type = table          
            
            if (data_type == 'client'):                
                  globvar = globvar + 1
                  clientForm = ClientForms(request.POST)
                  if type=="True":
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
                  type_compte = request.POST['type_compte']
                  endettementForm = EndettementForm(request.POST)


            print(globvar)
            if(globvar==4):
                  client_check = clientForm.is_valid()
                  emploi_check = emploiForm.is_valid()
                  place_check  = placeForm.is_valid()
                  dette_check  = endettementForm.is_valid()

  
                  if  client_check and place_check and emploi_check and dette_check :



                        new_endettement = Endettement(
                              phone_emploi            = endettementForm.cleaned_data.get('phone_emploi'),
                              nom_responsable         = endettementForm.cleaned_data.get('nom_responsable'),
                              saisi                   = endettementForm.cleaned_data.get('saisi'),
                              faillite                = endettementForm.cleaned_data.get('faillite'),
                              charge                  = charges,
                              charge_sum              = endettementForm.cleaned_data.get('phone_emploi'),
                        )

                        new_endettement.save()

                        new_emploi = Emploi(
                              denomination            = emploiForm.cleaned_data.get('denomination'),
                              nom_societe             = emploiForm.cleaned_data.get('nom_societe'),
                              adresse                 = emploiForm.cleaned_data.get('adresse'),
                              ville                   = emploiForm.cleaned_data.get('ville'),
                              pays                    = emploiForm.cleaned_data.get('pays'),
                              salaire_m               = emploiForm.cleaned_data.get('salaire_m'),
                              anciennete              = emploiForm.cleaned_data.get('anciennete'),
                              poste_actu              = emploiForm.cleaned_data.get('poste_actu'),
                              autre_revenu            = emploiForm.cleaned_data.get('autre_revenu'),
                              autre_rev_sum           = emploiForm.cleaned_data.get('autre_revenu_sum'),
                              ancien_denomination     = emploiForm.cleaned_data.get('ancien_denomination'),
                              ancien_nom_societe      = emploiForm.cleaned_data.get('ancien_nom_societe'),
                              ancien_adresse          = emploiForm.cleaned_data.get('ancien_adresse'),
                              ancien_ville            = emploiForm.cleaned_data.get('ancien_ville'),
                              ancien_code_postal      = emploiForm.cleaned_data.get('ancien_code_postal'),                          
                              ancien_pays             = emploiForm.cleaned_data.get('ancien_pays'),
                              ancien_salaire_m        = emploiForm.cleaned_data.get('ancien_salaire_m'),
                              ancien_anciennete       = emploiForm.cleaned_data.get('ancien_anciennete'),

                        )

                        new_emploi.save()


                        new_place = Place(
                              adresse                 = placeForm.cleaned_data.get('adresse'),
                              ancienne_address        = placeForm.cleaned_data.get('ancienne_address'),
                              ville                   = placeForm.cleaned_data.get('ville'),
                              ancienne_ville          = placeForm.cleaned_data.get('ancienne_ville'),
                              pays                    = placeForm.cleaned_data.get('pays'),
                              ancienne_pays           = placeForm.cleaned_data.get('ancienne_pays'),
                              loyer                   = placeForm.cleaned_data.get('loyer'),
                              ancienne_loyer          = placeForm.cleaned_data.get('ancienne_loyer'),
                              code_postal             = placeForm.cleaned_data.get('code_postal'),
                              ancienne_code_postal    = placeForm.cleaned_data.get('ancienne_code_postal'),
                              anciennete              = placeForm.cleaned_data.get('anciennete'),
                              ancienne_anciennete     = placeForm.cleaned_data.get('ancienne_anciennete'),
                        )

                        new_place.save()

                        # Register either the client or the cosigner

                        if type=="True":
                              # Storing a new Client
                              new_client = Client(
                                    societe                 = request.user.societe,
                                    User                    = request.user,
                                    nom                     = clientForm.cleaned_data.get('nom'),
                                    prenom                  = clientForm.cleaned_data.get('prenom'),
                                    email                   = clientForm.cleaned_data.get('email'),
                                    phone_1                 = clientForm.cleaned_data.get('phone_1'),
                                    phone_2                 = clientForm.cleaned_data.get('phone_2'),
                                    how_connu               = clientForm.cleaned_data.get('how_connu'),
                                    date_naissance          = clientForm.cleaned_data.get('date_naissance'),
                                    ville_naissance         = clientForm.cleaned_data.get('ville_naissance'),
                                    type_piece_id           = clientForm.cleaned_data.get('type_piece_id'),
                                    numero_piece_id         = clientForm.cleaned_data.get('numero_piece_id'),
                                    pays_naissance          = placeForm.cleaned_data.get('pays'),
                                    parents                 = bool(parents),
                                    proprietaire            = bool(proprietaire),
                                    place                   = new_place,
                                    emploi                  = new_emploi,
                                    endettement             = new_endettement, 
                                    uid                     = int(random.random()*1000000000)                       
                              )

                              new_client.save()
                              
                              clientData = new_client

                        else:
                              # Saving and assigning a clients Cosigner
                              new_cosigner = Cosignataire(
                                    societe                 = request.user.societe,
                                    User                    = request.user,
                                    nom                     = clientForm.cleaned_data.get('nom'),
                                    prenom                  = clientForm.cleaned_data.get('prenom'),
                                    email                   = clientForm.cleaned_data.get('email'),
                                    phone_1                 = clientForm.cleaned_data.get('phone_1'),
                                    phone_2                 = clientForm.cleaned_data.get('phone_2'),
                                    how_connu               = clientForm.cleaned_data.get('how_connu'),
                                    date_naissance          = clientForm.cleaned_data.get('date_naissance'),
                                    ville_naissance         = clientForm.cleaned_data.get('ville_naissance'),
                                    type_piece_id           = clientForm.cleaned_data.get('type_piece_id'),
                                    numero_piece_id         = clientForm.cleaned_data.get('numero_piece_id'),
                                    pays_naissance          = placeForm.cleaned_data.get('pays'),
                                    parents                 = bool(parents),
                                    proprietaire            = bool(proprietaire),
                                    place                   = new_place,
                                    emploi                  = new_emploi,
                                    endettement             = new_endettement,                        
                              )
                              new_cosigner.save()
                              
                              nom                     = client_interet.split(' ')[0]
                              prenom                  = client_interet.split(' ')[1:]
                              prenom                  = ' '.join(prenom)
                              print('----------------------------------------')
                              print(nom)
                              print(prenom)
                              print('----------------------------------------')

                              client                  = Client.objects.filter(nom = nom, prenom = prenom)
                              if client:
                                    client = client[0]
                              else:
                                    print('***********************************')
                                    print('*******   Client not found ********')
                                    print('***********************************')


                              client.cosigner         = new_cosigner
                              client.save() 

                              print(nom)
                              print(prenom)
                              appointment_to_delete = Appointment.objects.filter(nom = nom)

                              if appointment_to_delete:
                                    appointment_to_delete = appointment_to_delete[0]

                              print(appointment_to_delete)

                              article_interet       = appointment_to_delete.article_dinteret           


                              # Creating the Clients Dossier

                              article_interet          = article_interet.split('-')[-1]
                              article                  = Article.objects.filter(nom = article_interet.split('-')[-1])                   

                              if article:
                                    article = article[0]
                                    print(article)
                                    # Creating Client forms
                                    new_credit = Credit(
                                         article              = article,
                                         societe              = request.user.societe,             
                                    )

                                    new_credit.save()

                                    # Creating the clients facture after applied
                                    new_facture = Facture(
                                          article             = article,
                                          User_editeur        = request.user,
                                          statut              = "OM",
                                          num_facture         = "",
                                          somme               = article.frais_montage
                                    )
                                    new_facture.save()


                                    new_dossier = Dossier(
                                          societe                 = request.user.societe,             
                                          User                    = request.user,             
                                          client                  = client,
                                          credit                  = new_credit,
                                          article_interet         = article,
                                          facture                 = new_facture,        
                                          statut                  = 'OM',
                                          coeff_recouv            = 0,   
                                          pin                     = 0,    
                                          verifie                 = False, 
                                          uid                     = int(random.random()*1000000000)
                                          )

                                    new_dossier.save()
                                    currentDossier = new_dossier
                              appointment_to_delete.delete()


                        new_compte_endettement = CompteEndettement(
                              endettement             = new_endettement,
                              nom_banque              = nom_banque,
                              type_compte             = type_compte,
                              compte                  = compte,
                              nom_compte              = endettementForm.cleaned_data.get('nom_compte'),
                        )

                        new_compte_endettement.save()

                        new_preendettement = PretEndettement(
                              endettement             = new_endettement,
                              nom_banque              = nom_banque,
                              type_pret               = endettementForm.cleaned_data.get('type_pret'),
                              reste                   = endettementForm.cleaned_data.get('reste'),
                              mensualite              = endettementForm.cleaned_data.get('mensualite'),
                              nom_banque_1            = endettementForm.cleaned_data.get('nom_banque_1'),
                              type_pret_1             = endettementForm.cleaned_data.get('type_pret_1'),
                              reste_1                 = endettementForm.cleaned_data.get('reste_1'),
                              mensualite_1            = endettementForm.cleaned_data.get('mensualite_1'),
                              nom_banque_2            = endettementForm.cleaned_data.get('nom_banque_2'),
                              type_pret_2             = endettementForm.cleaned_data.get('type_pret_2'),
                              reste_2                 = endettementForm.cleaned_data.get('reste_2'),
                              mensualite_2            = endettementForm.cleaned_data.get('mensualite_2'),
                              date                    = endettementForm.cleaned_data.get('date'),

                        )

                        # new_preendettement.save()
                        # return HttpResponse('success')
                  else:
                        errors = f'Info Perso Client <br />{clientForm.errors}<br />Info Address Client <br />{placeForm.errors}<br />Info Emploi <br /> {emploiForm.errors} <br /> Info Endettement <br /> {endettementForm.errors} <br /> '                   
                       
                        return HttpResponse(errors)

            return HttpResponse('')

@login_required
def save_credit(request,dossier):
      matching_dossier = Dossier.objects.filter(uid=int(dossier))
      if matching_dossier:
            client_dossier = matching_dossier[0]
            credit         = client_dossier.credit
            credit.accompte         = request.POST['accompte']
            credit.taux             = request.POST['taux']
            credit.somme_payee      = request.POST['total']
            credit.frais_dossier    = request.POST['frais_dossier']
            credit.autre_frais      = request.POST['frais_autre']  
            credit.montant          = request.POST['paiement_mensuel']
            credit.date_fin         = request.POST['date_fin']
            
            credit.save()

            return HttpResponse('hello')



@login_required
def sendMail(request):
      if(request.method == 'POST' and request.user.poste == section):
            print(request.POST)
             
            send_mail(
                  "Django Email Test",
                  "Yo, hello from the real world, it just so happens that i am testing out django right now", # message
                  "karlsedoide@gmail.com",# from email
                  ['dzekarlson@gmail.com'],# To mail
                  fail_silently=False
            )
      else:
            pass



@login_required
def makePdf(request,name):
      if(request.user.poste == section):
            print('--------------------------')
            print('whats  up here')
            print(name)
            print('--------------------------')
            buf = io.BytesIO()

            # create canvas
            c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
            c.translate(cm,cm)
            #create a text object
            textob = c.beginText()
            textob.setTextOrigin(inch,inch)
            textob.setFont("Helvetica",14)

            # Add some lines of text
            if name=='authorisation':
                  text = '''
                  <img src="" height="500", width="300" />
                  Je soussigné ___________________ avoir appliqué pour un crédit à la consommation et autorise WEND PUIRE DISTRIBUTION et ses partenaires à faire des recherches concernant mon passé, mon emploi et d'autres informations qu'ils jugeront nécessaires., et tout cela dans le but de mieux évaluer les risques qu'ils pourraient encourir en octroyant un crédit. Je reconnais aussi que tout autre institution financière à laquel ils pourraient faire recours utilisera le même processus. J'accepte aussi d'être transféré de terrain, de site, de région, de banque ou di'institution financière, sans dédommagement si pour des raisons personnelles, WEND  PUIRE DISTRIBUTION en jugeait l'utilité.
                  L'institution financière sous citée pourrait être celle qui est responsable du futur contrat de financement concernant ma cession si WEND PUIRE DISTRIBUTION leur transmettait mon dossier, et je m'engage par la présente à me conformer aux normes, conditions et termes de cette nouvelle institution. Je suis par là notifié que mon application pour crédit consommateur pourrait leur être soumise.\n Institution financière : ___________________ Toutes
                  '''
            elif name == "recapitulatif":
                  pass
            elif name == "facture":
                  pass
            elif name == "engagement":
                  pass
            elif name == "ppe_imp":
                  pass
            elif name == "ppr_imp":
                  pass
            elif name == "pvi_imp":
                  pass
            elif name == "ct_imp":
                  pass
            else:
                  pass

            wraped_text = "\n".join(wrap(text, 70)) # 80 is line width
            textob.textLines(wraped_text)

            c.drawText(textob)
            c.showPage()
            c.save()
            buf.seek(0)

            return FileResponse(buf, as_attachment=True, filename=f"{name}.pdf")
            # pdf = FPDF('P', 'mm', 'Letter')
            # print(request.POST)
            # pdf.add_page()
            # pdf.set_font('helvetica','',16)
            # pdf.cell(40,11,request.POST['top_info'])
            # pdf.call(40,11,request.POST['bottom_info'])
            # pdf.output('pdf_1.pdf')
            # return HttpResponse(' ')



@login_required
def vente(request):
      global currentDossier
      dossier_uid = None
      if(request.user.poste == section):
            if request.method == 'POST':
                  print(request.POST)
                  dossier_uid = int(request.POST['dossier_id'])
                  currentDossier = Dossier.objects.filter(uid=dossier_uid)[0]
                  return render(request, 'transac/tvente.html', { 'title': 'Espace vente','client':clientData,'dossier':currentDossier})

            return render(request, 'transac/tvente.html', { 'title': 'Espace vente','client':clientData,'dossier':currentDossier})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def penalties(request):
      if(request.user.poste == section):


            all_info = Dossier.objects.all()
            
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range

            return render(request, 'transac/tpenalties.html', { 'title': 'Pénalités','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def payments(request):
      if(request.user.poste == section):
            filterby = Q(statut="P1") | Q(statut="A")
            all_info = Dossier.objects.filter(filterby)
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter(filterby)
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range


            return render(request, 'transac/tpaiement.html', { 'title': 'Paiements','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def mutations(request):
      if(request.user.poste == section):

            all_info = Dossier.objects.all()
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range

            return render(request, 'transac/tmutations.html', { 'title': 'Mutations','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def restructure(request):
      if(request.user.poste == section):
            all_info = Dossier.objects.all()
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range

            return render(request, 'transac/trestructurations.html', { 'title': 'Restructurations','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def plan(request):
      if(request.user.poste == section):
            all_info = Dossier.objects.all()
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range

            return render(request, 'transac/tpml.html', { 'title': 'Plan de masse local','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




# @login_required 
def dossiers_credit(request):
      if(request.user.poste == section):
            all_info = Dossier.objects.all()
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range
        
            return render(request, 'transac/tdc.html', { 'title': 'Dossiers crédits (DC)','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")




@login_required
def dossiers(request):
      if(request.user.poste == section):
            all_info = Dossier.objects.all()
        
            # CODE FOR PAGINATOR BELLOW
            dossier_objects = Dossier.objects.filter()
            paginator = Paginator(dossier_objects,1)
            page = request.GET.get('page',1)

            try:
                  all_info = paginator.page(page)
            except PageNotAnInteger:
                  all_info = paginator.page(1)
            except EmptyPage:
                  all_info = paginator.page(paginator.num_pages)

            page_list = all_info.paginator.page_range
            return render(request, 'transac/tdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)','page_list': page_list, 'page': page, "all_dossier": all_info})
      else:
            return redirect(f"/login?next=/{section}/")



# ENDPOINTS FOR PENALITE BELLOW

@login_required
@api_view(['GET'])
def paginate_penalite(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
    
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
    
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
    
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
    
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
    
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
     
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter()[starting_number:ending_number]
     
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
    coeff_recouv =  request.query_params.get('coeff_recouv', None)
    appele_recouvre = request.query_params.get('appele_recouvre', None)
    
    # FOR SEARCH FIELD BELLOW
    search_table = request.query_params.get('search_table', None)
    print('GOT HERE IN GET CAISSE')
    # print(prenom)
    caisse_info = Dossier.objects.all()

    if search_table:
        lookups = Q(client__uid__icontains=search_table) | Q(client__phone_1__icontains=search_table) | Q(client__nom__icontains=search_table) | Q(client__prenom__icontains=search_table) | Q(uid__icontains=search_table) | Q(statut__icontains=search_table) | Q(coeff_recouv__icontains=search_table) | Q(appele_recouvre__icontains=search_table) | Q(dernier_appel__icontains=search_table)
        
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
    id = request.query_params.get('id',None)
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
    id = request.POST.get('id',None)
    status = request.POST.get('status', None)
    dossier = Dossier.objects.get(pk=id)
    
    # facture = Facture.objects.get(pk=dossier.id)
    # dossier

    # GENERATE FACTURE 

    dossier.statut = status
    dossier.save()

    # print('INFO BELLOW')
    # print(id)
    # print(status)

    return Response({}) 



# SET PERCENT FOR FACTURE
@login_required
@api_view(['POST'])
def set_facture_penalty(request):
    # id = request.query_params.get('id',None)
    id = request.POST.get('id',None)
    type_of_amount = request.POST.get('type', None)
    value = request.POST.get('value',None)

    facture = Facture.objects.get(pk=id)

    if(type_of_amount == 'PERCENT'):
        # GET FACTURE AND CALCULATE PERCENT
        sum = int(facture.somme) * int(value) / 100
        facture.penalty_somme = sum
        facture.save()
    else:
        # GET FACTURE AND SUM AMOUNT
        sum = int(facture.somme) + int(value)
        facture.penalty_somme = sum
        facture.save()
    
    
    # facture = Facture.objects.get(pk=dossier.id)
    # dossier

    # GENERATE FACTURE 

    # print('INFO BELLOW')
    # print(id)
    # print(status)

    return Response({}) 