# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Planning import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    path('func_Planning/', views.func_Planning, name='func_Planning'),
    path('render_fihas/', views.render_fihas, name='renderfihas'),
    #Calendar & index settings
    

    #Security Settings
    

    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]