# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Payments import views

urlpatterns = [
    
    # The home page
    path('payments/', views.payments, name='payments'),       
]