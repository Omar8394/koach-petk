from ast import Pass, Try
from cgitb import html
from inspect import ismodule
from logging import exception
from multiprocessing import context
from turtle import ht
from django.contrib.auth.decorators import login_required
from django.forms.utils import pretty_name
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseForbidden
from django import template
from django.db.models import Q
from django.db.models.aggregates import Count
import json, math
from django.core.paginator import Paginator
from requests import request

from ..App.models import ConfMisfavoritos


from core import settings
from datetime import datetime

# Create your views here.

def mostrarfavoritos(request): 
    context = {}

    if request.method == "POST":
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:
                
                data = json.load(request)

                if data['acceso'] == 'show':

                    tab_data = ConfMisfavoritos.objects.all()
                    
                    context = {'data':tab_data}
                
                    html_template = loader.get_template( 'App/Favorito/mostrarFavoritos.html' )
                    return HttpResponse(html_template.render(context, request))
                
                if data['acceso'] == 'vaciar':

                    for item in data['idCheckbox']:
                        
                        favoritos = ConfMisfavoritos.objects.filter(pk=data['idCheckbox'][item])
                        favoritos.delete()
                
                    return JsonResponse({"message":"vacio"})

                if data['acceso'] == 'delete':

                    for item in data['idCheckdelete']:
                        
                        favoritos = ConfMisfavoritos.objects.filter(pk=data['idCheckdelete'][item])
                        favoritos.delete()
                
                    return JsonResponse({"message":"delete"})

                if data['acceso'] == 'edit':

                    favoritos = ConfMisfavoritos.objects.get(pk=int(data['item']))
                    favoritos.descripcion_url = data['item1']
                    favoritos.save()
                
                    return JsonResponse({"message":"edit"})
    
    
 
def añadirFavoritos(request):    
    context = {}

    if request.method == "POST":
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:
                data= json.load(request)

                if data['acceso'] == 'validar':
                    tab_data = ConfMisfavoritos.objects.filter(direccion_url=data['item']).count()
                    
                    return JsonResponse({"num":tab_data})

                if data['acceso'] == 'save':
                    tab_data = ConfMisfavoritos.objects.filter(direccion_url=data['item']).count()

                    if tab_data == 0:

                        favoritos = ConfMisfavoritos()

                        favoritos.idpublic=2
                        favoritos.direccion_url=data["item"]
                        favoritos.descripcion_url=data["item1"]

                        favoritos.save()

                        return JsonResponse({"message":"Perfect"})
                    else:
                        return JsonResponse({"message":"existe"})



                
                