# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Organizational_network import views

urlpatterns = [
 path('index_nodos/', views.index_nodos, name="index_nodos"), 
 path('modalAddgrupos/', views.modalAddgrupos, name="modalAddgrupos"), 
 path('renderGrupoPadre/', views.renderGrupoPadre, name="renderGrupoPadre"), 
 path('renderHijos/', views.renderHijos, name="renderHijos"), 
 path('Grupos_integrantes/<str:elemento>/', views.Grupos_integrantes, name="Grupos_integrantes"),
 path('saveintegrantes', views.saveintegrantes, name="saveintegrantes"),
 path('ModalAdddatos', views.ModalAdddatos, name="ModalAdddatos"),
 path('ModalStatus', views.ModalStatus, name="Modalstatus"),
 path('renderstat', views.renderstat, name="renderstat"),
 path('Modaltransfer', views.Modaltransfer, name="Modaltransfer"),
 path('RenderListanodos', views.RenderListas, name="RenderListasnodos"),
 path('plan_nodo/<str:grupo>/', views.plan_nodo, name="plan_nodo"),
 path('getcomponentsxplan/', views.getcomponentsxplan, name="getcomponentsxplan"),
 path('getestru_components/', views.getestru_components, name="getestru_components"),
 path('Saveestrutura_plan/', views.Saveestrutura_plan, name="Saveestrutura_plan"),
 path('mapamundi_nodos/', views.mapamundi_nodos, name="mapamundi_nodos"),
 path('Modalverpais/', views.Modalverpais, name="Modalverpais"),
 path('grupos_mundo/', views.grupos_mundo, name="grupos_mundo"),
]