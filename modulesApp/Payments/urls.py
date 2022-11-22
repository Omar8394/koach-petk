# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Payments import views

urlpatterns = [
    
    # The home page
    path('get_metodo_pgs/', views.get_metodo_pgs, name='get_metodo_pgs'),
    path('get_formPgPaypal/', views.get_formPgPaypal , name='get_formPgPaypal'),  
    path('payments/', views.payments, name='payments'),
    path('get_formPayments/', views.get_formPayments, name='get_formPayments'),
    path('get_buscarpublic/', views.get_buscarpublic, name='get_buscarpublic'),
    path('get_contenido_tab_beneficiario/', views.get_contenido_tab_beneficiario, name='get_contenido_tab_beneficiario'),
    path('get_sava_transferencia/', views.get_sava_transferencia, name='get_sava_transferencia'),

]