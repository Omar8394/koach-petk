# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Planning import views

app_name = "planning"
urlpatterns = [

    path('func_Planning/', views.func_Planning, name='func_Planning'),
    path('render_fihas/', views.render_fihas, name='renderfihas'),
    path('testfi/', views.testfi, name='testfi'),
    path('guardarFicha/', views.guardarFicha, name='guardarFicha'),
    path('eliminarFicha/', views.eliminarFicha, name='eliminarFicha'),
    

    # modales    
    path('modalFicha/', views.modalFicha, name='modalFicha'),

    # metodos
    path('validarNombreFicha/', views.validarNombreFicha, name='validarNombreFicha'),

]