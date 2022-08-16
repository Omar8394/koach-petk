# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Comunication import views

urlpatterns = [
    
    # The home page
    path('Comunication/Boletin/createBoletin/', views.createBoletin, name='createBoletin'),
     path('homeViews/', views.HomeViews, name='homeviews'),
    path('addboletin/', views.addboletin, name='addboletin'),
     
    path('Comunication/Boletin/acciones_boletin/', views.acciones_boletin, name='acciones_boletin'),
    path('Comunication/Boletin/edit_boletin/<int:id>', views.edit_boletin, name='edit_boletin'),
    path('Comunication/Boletin/edit_boletin_save/', views.edit_boletin_save, name='edit_boletin_save'),    
    path('Comunication/Boletin/showBoletin/', views.showBoletin, name='showBoletin'),
    path('Comunication/Boletin/test/', views.emailTest, name='emailtest'),
    # path('Comunication/Boletin/pruebaCarusel/', views.pruebaCarusel, name='pruebaCarusel'),
    
       
]