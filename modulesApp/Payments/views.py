import json
import math
import os
import shutil
from datetime import datetime
from decimal import *
#from msilib.schema import PublishComponent
from multiprocessing import context

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from core import settings

from ..App.models import AppPublico, ConfTablasConfiguracion
from ..Payments.models import Pagos_regpagos

# Create your views here.

def get_metodo_pgs(request):

    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['acceso'] == 'show':
                    metodo_pgs=ConfTablasConfiguracion.obtenerHijos("method_pgs")
                    
                    context={'metodo_pgs':metodo_pgs}
                    html_template= (loader.get_template('Payments/get_metodo_pgs.html'))

                    return HttpResponse(html_template.render(context, request))


def payments(request):
    
    concepto_pgs=ConfTablasConfiguracion.obtenerHijos("concepto_pgs")
    metodo_pgs=ConfTablasConfiguracion.obtenerHijos("method_pgs")
    fech_act=datetime.today().strftime('%Y-%m-%d')
    
    html_template= (loader.get_template('Payments/payments.html'))

    context={'metodo_pgs':metodo_pgs, 'concepto_pgs':concepto_pgs, 'fech_act':fech_act}
    return HttpResponse(html_template.render(context, request))



def get_formPgPaypal(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['acceso'] == 'show':
                    
                    context={}
                    html_template= (loader.get_template('Payments/formPayments.html'))

                    return HttpResponse(html_template.render(context, request))
                    

def get_formPayments(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['form_pg'] == 'transf_pgs':
                    
                    context={}
                    html_template= (loader.get_template('Payments/get_form_pg_transf.html'))

                    return HttpResponse(html_template.render(context, request))

                if data['form_pg'] == 'paypal_pgs':
                    
                    context={}
                    html_template= (loader.get_template('Payments/get_form_pg_payp.html'))

                    return HttpResponse(html_template.render(context, request))

def get_buscarpublic(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['acceso'] == 'buscar':
                    data= AppPublico.objects.all()
                    context={'data':data}
                    html_template= (loader.get_template('Payments/get_buscar_public.html'))

                    return HttpResponse(html_template.render(context, request))

def get_contenido_tab_beneficiario(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data_req= json.load(request)
                if data_req['acceso'] == 'show':
                    lista=[]
                    
                    for id_public in data_req['idCheckbox']: 
                        publico= list(AppPublico.objects.filter(idpublico=id_public))
                        for public in publico:
                            # print(public.nombre)
                            lista.append({'nombre':public.nombre, 'apellido': public.apellido}) 

                    context={'data':lista}
                    html_template= (loader.get_template('Payments/contenido_tab_beneficiario.html'))

                    return HttpResponse(html_template.render(context, request))

def get_sava_transferencia(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                data_req= json.load(request)
                
                user_public= list(AppPublico.objects.filter(user_id=request.user).values())
                
                fech_act=datetime.today().strftime('%Y-%m-%d')

                fk_conceptopg=list(ConfTablasConfiguracion.objects.filter(valor_elemento__contains=data_req["id_concepto_pg"]).values())
                fk_metodopg=list(ConfTablasConfiguracion.objects.filter(valor_elemento__contains=data_req["id_metodo_pg"]).values())

                pay_save = Pagos_regpagos()

                if data_req["acceso"] == "save":

                    for id_public in data_req['idCheckbox']:
                        
                        pay_save.fechaPago=str(fech_act)
                        pay_save.referencia=data_req["data"]["v_referencia"]
                        pay_save.confirmado=0
                        pay_save.montopagado=Decimal(data_req["data"]["v_monto"])
                        pay_save.codigohash=""
                        pay_save.beneficiario=int(id_public)
                        pay_save.fkStatusPago_id=1
                        pay_save.fkconceptopago_id=int(fk_conceptopg[0]['id_tabla'])
                        pay_save.fkmetodopago_id=int(fk_metodopg[0]['id_tabla'])
                    
                        pay_save.fkpublic_id=int(user_public[0]['idpublico'])
                        
                        
                        pay_save.save()

                        
                    return JsonResponse({"message":"okey"})

        
                return JsonResponse({"message":"error"}, status=500)
                



