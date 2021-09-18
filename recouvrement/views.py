from django.template.loader import get_template
from rest_framework.response import Response
from transac.serializers import DossierSerializer
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .decorators import unauthenticated_user, allowed_users
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
from main.models import Client, Facture, Place, Emploi, Endettement, CompteEndettement, PretEndettement, Dossier, Cosignataire, Article, Appointment, Credit, Societe
from django.core.mail import send_mail
from xhtml2pdf import pisa
# Direction du recouvrement routes
# @unauthenticated_user
# @allowed_users(allowed_roles=['recouvrement'])
section = "recouvrement"


@login_required
def index(request):
    if(request.user.poste == section):

        return render(request, 'recouvrement/recouvrement.html', {'title': 'Recouvrement'})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
def etat_recouvrements(request):
    if(request.user.poste == section):
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='R1')  # | Q
        paginator = Paginator(dossier_objects, 3)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'recouvrement/direction/etat-recouvrement.html', {'title': 'Etat des Recouvrements', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")

# ENDPOINTS FOR CPML BELLOW


@login_required
@api_view(['GET'])
def paginate_etat(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    print("page Number: " + str(page))
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe)[
        starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_etat(request):
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


@ login_required
def contacts(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/gestion-contact.html', {'title': ' Gestion des contacts'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def litiges(request):
    if(request.user.poste == section):
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe) .filter(statut='RT')  # | Q
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range
        return render(request, 'recouvrement/direction/gestion-litige.html', {'title': ' Gestion des litiges', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
@api_view(['GET'])
def paginate_litiges(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    print("page Number: " + str(page))
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe)[
        starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_litiges(request):
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


@ login_required
def finalisations(request):
    if(request.user.poste == section):
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe).filter(statut='FN')  # | Q
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range
        return render(request, 'recouvrement/direction/finalisations.html', {'title': ' Finalisation', 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@login_required
@api_view(['GET'])
def paginate_finalisations(request):
    # pagination bellow
    print('GOT HERE IN PAGINATE')
    page = request.GET.get('page', None)
    page = int(page)
    print("page Number: " + str(page))
    starting_number = (page-1)*1
    ending_number = page*1

    results = Dossier.objects.filter(societe__nom=request.user.societe)[
        starting_number:ending_number]

    serialized = DossierSerializer(results, many=True)
    # print('SERIALIZED DATA BELLOW')
    # print(serialized.data)
    return Response(serialized.data)


@login_required
@api_view(['GET'])
def get_finalisations(request):
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


@login_required
def getPdf(request):
    # dossier_uid = int(dossier)
    # if dossier_uid < 1000000:
    #     dossier = Dossier.objects.get(id=dossier_uid)
    # else:
    #     dossier = Dossier.objects.get(uid=dossier_uid)
    # print(dossier)
    # print(name)
    # template_path = None
    # if name == 'facture':
    #     template_path = 'recouvrement/finalisation/vente_facture.html'
    # if name == "engagement":
    #     template_path = 'recouvrement/finalisation/engagement.html'
    # if name == "ppe_imp":
    #     template_path = 'recouvrement/finalisation/ppe_imp.html'
    # if name == "ppr_imp":
    #     template_path = 'recouvrement/finalisation/ppr_imp.html'
    # if name == "pvi_imp":
    #     template_path = "recouvrement/finalisation/pvi_imp.html"
    # if name == "ct_imp":
    #     template_path = "recouvrement/finalisation/ct_imp.html"
    # if name == "bal_imp":
    #     template_path = "recouvrement/finalisation/bal_imp.html"
    # if name == "ppe_imp":
    #     template_path = "recouvrement/finalisation/ppe_imp.html"

    # context = {'dossier': dossier}
    context = {}

    template_path = "recouvrement/finalisation/certificate_felicitation.html"

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


@ login_required
def rapports(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/direction/rapports.html', {'title': ' Rapports'})
    else:
        return redirect(f"/login?next=/{section}/")


# Etats dossiers routes

@ login_required
def etat_dossiers_recouvrement(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/recouvrement.html', {'title': ' Etat des recouvrements'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def etat_dossiers_statistique(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/statistique.html', {'title': ' Etat statistique'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def etat_profil_dossiers(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/profil-dossiers.html', {'title': 'Profil dossiers'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def etat_dossiers_recouvrement_complets(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/etats-dossiers/etats-complets.html', {'title': ' Etat dossiers complets'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # Contact routes
def contact_rappel(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/rappel.html', {'title': ' Appel Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def contact_sms(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/sms.html', {'title': ' SMS Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def contact_autosms(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/autosms.html', {'title': 'Auto SMS'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def contact_emails(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/emails.html', {'title': ' Email Manuels'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def contact_autoemails(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/autoemails.html', {'title': ' Auto Email'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def contact_annotation(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/contacts/annotation.html', {'title': ' Annotation'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # Gestion finalisation routes
def gestion_verification_paiement(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/verification-paiement.html', {'title': 'Verification de fin de paiement'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_attestation(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/attestation.html', {'title': ' Attestion de fin de paiement'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_pml(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/pml.html', {'title': 'Emissions plans de masses locaux'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_felicitations(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/felicitations.html', {'title': 'Certificats de félicitations'})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_attributions(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/gestion-finalisation/attributions.html', {'title': "Certificats d'attributions"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # (proprieraires terriens, modif restructure) routes
def prop_terriens(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/credit-prop-terriens.html', {'title': "Dossiers crédits prop. terriens"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def modif_restructure(request):
    if(request.user.poste == section):
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(
            societe__nom=request.user.societe)  # .filter(statut='RT')  # | Q
        paginator = Paginator(dossier_objects, 1)
        page = request.GET.get('page', 1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'recouvrement/modif-restructure.html', {'title': "Modification & Restructuration", 'page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # annulation routes
def annulation_auto(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/automatique.html', {'title': "Annulation automatique"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def annulation_courrier(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/courrier.html', {'title': "Annulation par courrier"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def annulation_finalisation(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/annulation/finalisation.html', {'title': "Annulation finalisation"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # delocalisation routes
def delocalisation_auto(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/automatique.html', {'title': "Delocalisation automatique"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def delocalisation_courrier(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/courrier.html', {'title': "Delocalisation par courrier"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def delocalisation_finalisation(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/delocalisation/finalisation.html', {'title': "Delocalisation finalisation"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # sinistre routes
def gestionpr_1(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestionpr-1.html', {'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestionpr_2(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestionpr-2.html', {'title': "Gestion sinistre phase 2 (acceptée)"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_vi_1(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-vi-1.html', {'title': "Gestion sinistre phase 1 (Reception sinistre et recherche)"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_vi_2(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-vi-1.html', {'title': "Gestion sinistre phase 2 (acceptée)"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def gestion_rejets(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/sinistre/gestion-rejets.html', {'title': "Gestion sinistre phase 2 (rejetée)"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required  # repechage routes
def repechage_auto(request):
    if(request.user.poste == section):
        if(request.method == "POST"):
            print(request.POST)
        return render(request, 'recouvrement/repechage/automatique.html', {'title': "Repêchage 1"})
    else:
        return redirect(f"/login?next=/{section}/")


@ login_required
def repechage_2(request):
    if(request.user.poste == section):
        return render(request, 'recouvrement/repechage/repechage2.html', {'title': "Repêchage 2"})
    else:
        return redirect(f"/login?next=/{section}/")
