# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Payments import views

urlpatterns = [
    
    # The home page
    path('get_metodo_pgs/', views.get_metodo_pgs, name='get_metodo_pgs'),
    path('get_formPayments/', views.get_formPayments , name='get_formPayments'),  
    path('payments/', views.payments, name='payments'),
    path('get_formPgTransf/', views.get_formPgTransf, name='get_formPgTransf'),
        
]