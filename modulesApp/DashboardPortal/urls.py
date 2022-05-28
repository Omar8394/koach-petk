# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.DashboardPortal import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('Dashboard', views.Dashboard, name='Dashboard'),

    #Calendar & index settings
    

    #Security Settings
    

    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]