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
    path('capacitacion_student', views.indexstudent, name='capacitacion_student'),
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
    path('modalNewsesiones/', views.getModalNewsesiones, name="modalNewsesiones"),
    path('modalNewtest/', views.getModalNewtest, name="modalNewtest"),
    path('renderNewtest/', views.renderModalNewTest, name="renderNewtest"),
    path('pageslessons/', views.pageslessons, name="pageslessons"),
    path('programasrsesion/', views.programarsesiones, name="programasrsesion"),
    path('savepages/', views.savepages, name="savepages"),
    path('savesesionprogramas/', views.savesesionprogramas, name="savesesionprogramas"),
    path('modalResourcesBank/', views.getModalResourcesBank, name="modalResourcesBank"),
    path('contenidoRecursos/', views.getContentRecursos, name="contenidoRecursos"),
    path('renderpaginas/', views.renderpaginas, name="renderpaginas"),
    path('rendersesiones/', views.rendersesiones, name="rendersesiones"),   
    path('previewlessons/', views.previewlessons, name="previewlessons"),
    path('preRequirements/', views.preRequirements, name="preRequirements"),
    path('comboboxpro/', views.comboboxpro, name='comboboxpro'),
    path('renderListasPublic', views.renderListasPublic, name='renderListasPublic'),
    path('requirementos/', views.requirementos, name="requirementos"),
    path('testinit/', views.testinit, name="testinit"),
    path('rendertest/', views.rendertest, name="rendertest"),
    path('renderizarnuevaspre/', views.renderizarnuevaspre, name="renderizarnuevaspre"),
    path('renderpreguntas/', views.renderpreguntas, name="renderpreguntas"),
    #path('modalChooseTypeQuestion/', views.getModalChooseTypeQuestion, name="modalTypeQuestion"),
    path('getModalbloques/', views.getModalbloques, name="getModalbloques"),
    path('modalNewSimple/', views.getModalNewSimple, name="modalNewSimple"),
    path('EditNewSimple/', views.EditNewSimple, name="EditNewSimple"),
    path('EditNewMultiple/', views.EditNewMultiple, name="EditNewMultiple"),
    path('modalNewMultiple/', views.getModalNewMultiple, name="modalNewMultiple"),
    path('modalAddQuestion/', views.getModalQuestion, name="modalAddQuestion"),
    path('modalNewTof/', views.getModalNewTof, name="modalNewTof"),
    path('getModalNewparrafo/', views.getModalNewparrafo, name="getModalNewparrafo"),
    path('EditNewtof/', views.EditNewtof, name="EditNewtof"),
    path('EditNewparrafo/', views.EditNewparrafo, name="EditNewparrafo"),
    path('sortPreguntas/', views.sortPreguntas, name="sortPreguntas"),
    path('renderstudent/', views.renderstudent, name="renderstudent"),
    path('renderstemas/', views.renderstemas, name="renderstemas"),
    path('logUser/', views.logUser, name="logUser"),
    path('verpaginas_student/', views.verpaginas_student, name="verpaginas_student"),
    path('imagesave/', views.imagesave, name="imagesave"),
    path('borrarImagenes/', views.borrarImagenes, name="borrarImagenes"),
    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]