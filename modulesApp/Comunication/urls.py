# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Comunication import views

urlpatterns = [
    
    # The home page
    path('Comunication/Boletin/createBoletin/', views.createBoletin, name='createBoletin'),
    path('Comunication/Boletin/showBoletin/', views.showBoletin, name='showBoletin'), 
    path('Comunication/Boletin/addBoletinModal/', views.addBoletinModal, name='addBoletinModal'),
       
]