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
    path('createactividades/', views.createactividades, name='createactividades'),
    path('renderactividades/', views.renderactividades, name='renderactividades'),
    path('modalChooseActivity/', views.getModalChooseActivities, name='modalChooseActivity'),
    path('modalNewLesson/', views.getModalNewLesson, name="modalNewLesson"),
    path('modalNewhome/', views.getModalNewhomework, name="modalNewhome"),
    path('pageslessons/', views.pageslessons, name="pageslessons"),
    path('savepages/', views.savepages, name="savepages"),
    path('modalResourcesBank/', views.getModalResourcesBank, name="modalResourcesBank"),
    path('contenidoRecursos/', views.getContentRecursos, name="contenidoRecursos"),
    path('renderpaginas/', views.renderpaginas, name="renderpaginas"),
    path('previewlessons/', views.previewlessons, name="previewlessons"),
    path('preRequirements/', views.preRequirements, name="preRequirements"),
    path('comboboxpro/', views.comboboxpro, name='comboboxpro'),
    path('renderListasPublic', views.renderListasPublic, name='renderListasPublic'),
    path('requirementos/', views.requirementos, name="requirementos"), 
    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]