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

from ..App.models import ConfMisfavoritos


from core import settings
from datetime import datetime

# Create your views here.

def func_Planning(request): 
    context = {}

    html_template = loader.get_template( 'Planning/carpPlanning/starterpage.html' )
    return HttpResponse(html_template.render(context, request))
    
               
                
