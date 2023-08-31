# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.App import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    path('App/Favorito/mostrarfavoritos/', views.mostrarfavoritos, name='mostrarfavoritos'), 
    path('App/Favorito/añadirFavoritos/', views.añadirFavoritos, name='añadirFavoritos'),
    path('App/configuracion/', views.configuracion, name='configuracion'),
    path('App/settings/scales/', views.scales, name='scales'),
    path('App/settings/scalesGeAddModal/', views.scalesGeAddModal, name='modalScaleGeAdd'),
    path('App/settings/tabla', views.componentTabla, name='component_tabla'),   
    #Calendar & index settings
    path('App/settings/preferencias/', views.preferencias, name='preferencias'),
    path('App/settings/modalprefer/', views.getmodalprefer, name='modalprefer'),
    path('App/settings/saveprefer/', views.saveprefer, name='saveprefer'),
    path('App/settings/upprefer/', views.setprefer, name='updatepre'),
    path('App/settings/combobox/', views.combobox, name='combobox'),
    path('App/settings/tables/', views.tablesettings, name='tables'),
    path('App/settings/contentables/', views.getcontentablas, name='contentables'),
    path('App/settings/verhijos/', views.gethijos, name='verhijos'),
    path('App/settings/modalAddSetting/', views.getModalSetting, name="modalAddSetting"),
    path('App/settings/deletesetting/', views.deletehijos, name="deletesetting"),
    path('App/settings/editsetting/', views.edithijos, name="editsetting"),
    path('App/settings/managepersons/', views.managepersons, name="managepersons"),
    path('App/settings/unlockPublic/', views.unlockPublic, name='unlockPublic'),
    path('App/settings/lockPublic/', views.lockPublic, name='lockPublic'),
    path('App/settings/listaRol/', views.listaRol, name='listaRol'),
    path('App/settings/setRole/', views.setRole, name='setRole'),
    path('App/settings/paginar/', views.paginar, name='paginar'),
    #Security Settings
    

    # Scales
    

    # notificacioines
    
    
    # Matches any html file
    

]