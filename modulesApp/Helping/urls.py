# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Helping import views
app_name = "helping"
urlpatterns = [

    path('nuevo/', views.nuevo, name="nuevo"),  
    path('modalAddAyuda', views.modalAddAyuda, name='modalAddAyuda'),
    path('modalGuardarAyuda', views.modalGuardarAyuda, name='modalGuardarAyuda'),
    path('modalBuscarAyuda', views.modalBuscarAyuda, name='modalBuscarAyuda'),
    path('modalEliminarAyuda', views.modalEliminarAyuda, name='modalEliminarAyuda'),
    path('modalAddPagina', views.modalAddPagina, name='modalAddPagina'),
    path('modalPdf', views.modalPdf, name='modalPdf'),
    path('modalGuardarPagina', views.modalGuardarPagina, name='modalGuardarPagina'),
    path('modalHijosPagina', views.modalHijosPagina, name='modalHijosPagina'),
    path('modalEliminarHijoPagina', views.modalEliminarHijoPagina, name='modalEliminarHijoPagina'),
    path('modalAddCarruserl', views.modalAddCarruserl, name='modalAddCarruserl'),
    path('modalGuardarImagen', views.modalGuardarImagen, name='modalGuardarImagen'),
    path('modalGuardarPdf', views.modalGuardarPdf, name='modalGuardarPdf'),
    path('modalEliminarImagen', views.modalEliminarImagen, name='modalEliminarImagen'),
    path('modalPaginaMover', views.modalPaginaMover, name='modalPaginaMover'),
    

    path('validarTituloAyuda', views.validarTituloAyuda, name='validarTituloAyuda'),
]