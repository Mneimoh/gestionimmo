from django import forms
from django.core import paginator
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.utils.serializer_helpers import JSONBoundField
from .decorators import unauthenticated_user, allowed_users
from main.models import Appointment, Article
from .forms import AppointmentForms
from .filters import AppointmentFilter
from datetime import date

# NEW IMPORT BELLOW TESTING
from .serializers import AppointmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

#NEW IMPORTS FOR SEARCH INPUT
from django.db.models import CharField
from django.db.models import  Q


# NEW IMPORTS FOR PAGINATION
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

section = "accueuil"
# Create your views here.

@login_required
def index(request):
    if(request.user.poste == section):
        if(request.method == 'POST'):
            print('##########REQUEST BELLOW#############')
            print(request.POST)
            post_values = request.POST.copy()
            post_values['date_arrivee'] = '12/08/2020'
            post_values['heure_arrivee'] = '14:00'
            post_values['status'] = 'APT'
            appointment = AppointmentForms(post_values)
        
            if(appointment.is_valid()):
                # If appointment is valid then we want to save it to the database 
                print('APPOINTMENT IS VALID')
                appointment.save()
                return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels', 'new_appointment': True})
            else:
                print('###############Erros Bellow#################')
                print(appointment.errors)
                return render(request,'accueuil/appel.html', {'title': '', 'is_valid': False, })

        else:
            articles = Article.objects.all()

            return render(request,'accueuil/appel.html', { 'title': 'Enregistrement des appels','new_appointment': False, 'article_interet':articles})
        
    else:
        return redirect(f"/login?next=/{section}/")

@login_required
def rdv(request):
    if(request.user.poste == section):
        if(request.method == 'GET'):
            all_appointments = Appointment.objects.filter(status='APT')
            # Pass All Appoints To The table view and display them on the table
            #Add Filter Functionality
            # myFilter = AppointmentFilter(request.GET,queryset=all_appointments)
            # all_appointments = myFilter.qs
            # Bellow Is How To Get Appointment By Range
            # all_appointments = all_appointments.filter(date_redezvous__lt='2021-08-07')
            today = date.today()
            date_pass =  all_appointments.filter(date_redezvous__lt=f'{today}')
            date_tocome = all_appointments.filter(date_redezvous__gte=f'{today}')
            date_pass_count = len(date_pass)
            date_tocome_count = len(date_tocome)

            # CODE FOR PAGINATOR BELLOW
            appointment_objects = Appointment.objects.filter(status='APT')
            paginator = Paginator(appointment_objects,10)
            page = request.GET.get('page',1)

            try:
                appointments = paginator.page(page)
            except PageNotAnInteger:
                appointments = paginator.page(1)
            except EmptyPage:
                appointments = paginator.page(paginator.num_pages)
            
            page_list = appointments.paginator.page_range

            articles = Article.objects.all()

            return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous', 'page_list': page_list, 'page': page, 'appointments': appointments, 'date_tocome': date_tocome_count, 'date_pass': date_pass_count, 'article_interet':articles})

        else:
            #POST REQUEST
            return render(request,'accueuil/rdv.html', { 'title': 'Enregistrement des rendez-vous'})
    else:
        return redirect(f"/login?next=/{section}/")

# API CALL FUNCTIONS BELLOW

@login_required
@api_view(['GET'])
def paginate_appointments(request):
    # pagination bellow
    page = request.GET.get('page',None)
    page = int(page)
    starting_number = (page-1)*10
    ending_number = page*10

    results = Appointment.objects.filter()[starting_number:ending_number]
    serialized = AppointmentSerializer(results, many=True)
   
    return Response(serialized.data)

# @login_required
@api_view(['GET','PUT'])
def appointment(request):
    if(request.method == 'GET'):
        id = request.query_params.get('id',None)
        appointment = Appointment.objects.get(pk=id)
        
        if appointment:
            serialized = AppointmentSerializer(appointment)
            return Response(serialized.data)
        else:
            return Response({})
    elif(request.method == 'PUT'):
        print('############UPDATE DATA IN DB###########')
        
        print(request.POST.get('client_id'))
        client_id = request.POST.get('client_id')
        num_client = request.POST.get('num_client')
        date_arrivee = request.POST.get('date_arrivee')
        heure_arrivee = request.POST.get('heure_arrivee')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        article = request.POST.get('article')
        how_connu =request.POST.get('how_connu')

        appointment = Appointment.objects.get(pk=client_id)
        print('############APPOINTMENT BELLOW#############3')
        appointment.date_arivee = date_arrivee 
        appointment.heure_arrivee = heure_arrivee
        appointment.nom = nom
        appointment.prenom = prenom
        appointment.telephone = telephone
        appointment.article = article
        appointment.num_client = num_client
        appointment.how_connu = how_connu
        appointment.status = 'PQ'
        appointment.save()
        return Response({}) 
        

@login_required
@api_view(['GET'])
def get_appointments(request):
    nom = request.query_params.get('nom', None)
    prenom = request.query_params.get('prenom', None)
    num_client = request.query_params.get('num_client', None)
    telephone = request.query_params.get('telephone', None)
    how_connu = request.query_params.get('how_connu', None)
    date_dappel = request.query_params.get('date_dappel', None)
    heure_dappel =  request.query_params.get('heure_dappel', None)
    article_dinteret = request.query_params.get('article_dinteret', None)
    date_rendezvous = request.query_params.get('date_rendezvous', None)
    heure_rendezvous = request.query_params.get('heure_rendezvous', None)
    
    search_nom = request.query_params.get('search_nom', None)
    date_tocome = request.query_params.get('date_tocome', None)
    date_pass = request.query_params.get('date_pass', None)

    appointments = Appointment.objects.all()
    
    today = date.today()
    



    if search_nom:
        lookups = Q(nom__icontains=search_nom) | Q(prenom__icontains=search_nom) | Q(num_client__icontains=search_nom) | Q(telephone__icontains=search_nom) | Q(how_connu__icontains=search_nom) | Q(article_dinteret__icontains=search_nom) | Q(status__icontains=search_nom) | Q(heure_arrivee__icontains=search_nom)
       
        appointments = appointments.filter(lookups).distinct()
      
        print(appointments)
    if nom:
        appointments = appointments.all().order_by('nom')
    if prenom:
        appointments = appointments.all().order_by('prenom')
    if num_client:
        appointments = appointments.all().order_by('num_client')
    if telephone:
        appointments = appointments.all().order_by('telephone')
    if how_connu:
        appointments = appointments.all().order_by('how_connu')
    if date_dappel:
        appointments = appointments.all().order_by('date_dappel')
    if heure_dappel:
        appointments = appointments.all().order_by('heure_dappel')
    if article_dinteret:
        appointments = appointments.all().order_by('article_dinteret')
    if date_rendezvous:
        appointments = appointments.all().order_by('date_rendezvous')
    if heure_rendezvous:
        appointments = appointments.all().order_by('heure_rendezvous')
    
    if appointments:
        serialized = AppointmentSerializer(appointments, many=True)
        return Response(serialized.data)
    else:
        return Response({})
    