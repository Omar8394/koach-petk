# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.App import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    path('App/Favorito/mostrarfavoritos/', views.mostrarfavoritos, name='mostrarfavoritos'), 
    path('App/Favorito/añadirFavoritos/', views.añadirFavoritos, name='añadirFavoritos'),
    path('App/configuracion/', views.configuracion, name='configuracion'),
    
    #Calendar & index settings
    

    #Security Settings
    

    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]