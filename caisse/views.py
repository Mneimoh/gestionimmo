from transac.views import dossiers
from django.http import request
from accueuil import serializers
from caisse.serializers import DossierSerializer, FactureSerializer
from accueuil.views import appointment
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_users
from main.models import Dossier, Facture
# IMPORTS FOR SEARCH
from django.db.models import  Q

# NEW IMPORTS FOR PAGINATION
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


section = 'caisse'

@login_required
def index(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(statut='OM')
        
        # CODE FOR PAGINATOR BELLOW
        # GETTING JUST USERS THAT JUST OPENED ACCOUNT
        dossier_objects = Dossier.objects.filter(statut="OM")
        paginator = Paginator(dossier_objects,1)
        page = request.GET.get('page',1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request, 'caisse/caisse.html', {'title': 'Ouverture et montage de dossier', 'page_list': page_list, 'page': page, "all_dossier": all_info })
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpaiement(request):
    if(request.user.poste == section):
        all_info = Dossier.objects.filter(statut='A')
        
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(statut='A')
        paginator = Paginator(dossier_objects,1)
        page = request.GET.get('page',1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range


        return render(request,'caisse/cpaiements.html', { 'title': 'Paiements mensuels','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpenalites(request):
    if(request.user.poste == section):
        # GETTING JUST USERS WITH PENALTY STATUS TRUES
        all_info = Dossier.objects.filter(facture__penalty_status=True)
        
        # CODE FOR PAGINATOR BELLOW
        dossier_objects = Dossier.objects.filter(facture__penalty_status=True)
        paginator = Paginator(dossier_objects,1)
        page = request.GET.get('page',1)

        try:
            all_info = paginator.page(page)
        except PageNotAnInteger:
            all_info = paginator.page(1)
        except EmptyPage:
            all_info = paginator.page(paginator.num_pages)

        page_list = all_info.paginator.page_range

        return render(request,'caisse/cpenalites.html', { 'title': 'Pénalités','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def crestructurations(request):
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

        return render(request,'caisse/crestructurations.html', { 'title': 'Restructurations','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdelocalisations(request):
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

        return render(request,'caisse/cdelocalisations.html', { 'title': 'Délocalisations','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cmutations(request):
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

        return render(request,'caisse/cmutations.html', { 'title': 'Mutations','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cpml(request):
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
        
        return render(request,'caisse/cpml.html', { 'title': 'Plan de masse local','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdcpt(request):
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
        
        return render(request,'caisse/cdcpt.html', { 'title': 'Dossiers crédits propriétaires terriens (DCPT)','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")



@login_required
def cdc(request):
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


        return render(request,'caisse/cdc.html', { 'title': 'Dossiers crédits (DC)','page_list': page_list, 'page': page, "all_dossier": all_info})
    else:
        return redirect(f"/login?next=/{section}/")

from rest_framework.decorators import api_view
from rest_framework.response import Response

# ALL API CALLS ENDPOINTS BELLOW

# ENDPOINTS FOR CAISSE BELLOW
@login_required
@api_view(['GET'])
def paginate_caisse(request):
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
def get_caisse(request):
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






# ENDPOINTS FOR PAIEMENTS BELLOW

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



# ENDPOINTS FOR DELOCALISATIONS BELLOW

@login_required
@api_view(['GET'])
def paginate_delocalisations(request):
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
def get_delocalisations(request):
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



# ENDPOINTS FOR CPML BELLOW

@login_required
@api_view(['GET'])
def paginate_cpml(request):
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
def get_cpml(request):
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




# ENDPOINTS FOR CDCPT BELLOW

@login_required
@api_view(['GET'])
def paginate_cdcpt(request):
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
def get_cdcpt(request):
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



# ENDPOINTS FOR CDC BELLOW

@login_required
@api_view(['GET'])
def paginate_cdc(request):
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
def get_cdc(request):
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
def pay_facture_om(request):
    # id = request.query_params.get('id',None)
    id = request.POST.get('id',None)
    status = request.POST.get('status',None)
    # status = request.query_params.get('status',None)
    dossier = Dossier.objects.get(pk=id)
    
    facture = Facture.objects.get(pk=dossier.id)
    # dossier
    dossier.statut = status
    facture.statut = 'PAID'
    dossier.save()
    facture.save()


    return Response({}) 
