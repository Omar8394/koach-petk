from multiprocessing import context
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
import json, math
import os
import shutil
from core import settings
from django.core.files.storage import FileSystemStorage

from datetime import datetime

from ..App.models import ConfTablasConfiguracion

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

    html_template= (loader.get_template('Payments/payments.html'))

    context={'metodo_pgs':metodo_pgs, 'concepto_pgs':concepto_pgs}
    return HttpResponse(html_template.render(context, request))



def get_formPayments(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['acceso'] == 'show':
                    
                    context={}
                    html_template= (loader.get_template('Payments/formPayments.html'))

                    return HttpResponse(html_template.render(context, request))
                    

def get_formPgTransf(request):
    context={}
    if request.method == 'POST':
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            if request.body:
                
                data= json.load(request)
                if data['acceso'] == 'show':
                    
                    context={}
                    html_template= (loader.get_template('Payments/get_form_pg_transf.html'))

                    return HttpResponse(html_template.render(context, request))


