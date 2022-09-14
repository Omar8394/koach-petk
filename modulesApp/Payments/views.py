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

# Create your views here.

def payments(request):
    
    context={}

    html_template= (loader.get_template('Payments/payments.html'))

    return HttpResponse(html_template.render(context, request))



