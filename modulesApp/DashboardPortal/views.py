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
import json, math
from django.core.paginator import Paginator

from core import settings
from datetime import datetime

# Create your views here.

def index(request):
    
    context = {'mess':'Cristo me escuchas'}
    context['segment'] = 'index'
    
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def Dashboard(request):
    
    context = {}
    context['segment'] = 'Dashboard'
    
    html_template = loader.get_template( 'Dashboard_Portal/Dashboard.html' )
    return HttpResponse(html_template.render(context, request))