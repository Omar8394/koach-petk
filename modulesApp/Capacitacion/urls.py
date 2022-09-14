# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Capacitacion import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    path('', views.index, name='capacitacion'),
    path('saveunits/', views.indextwo, name='capacitaciontwo'),
    path('contenido_programas/', views.getcontentprogrmas, name='contenido_programas'),
    path('contenido_unidades/', views.getcontentunits, name='contenido_unidades'),
    path('contenido_cursos/', views.getcontentcursos, name='contenido_cursos'),
    path('modaladdcategoria/', views.modalagregarcategoria, name='modaladdcategoria'),
    path('modaladdprogram/', views.modalAddprogram, name='modaladdprogram'),
    path('addproceso/', views.Addproceso, name='addproceso'),
    path('modaladdproceso/', views.modalAddproceso, name='modaladdproceso'),
    path('modaladdmodulos/', views.modalAddmodulos, name='modaladdmodulos'),
    path('modaladdcursos/', views.modalAddcursos, name='modaladdcursos'),
    path('relation/', views.relation_componente, name='relation'),
    path('update_estrutura/', views.update_estrutura, name='update_estrutura'),
    path('componentsxestructura/', views.getcomponentsxestructura, name='componentsxestructura'),
    #Security Settings
    

    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]