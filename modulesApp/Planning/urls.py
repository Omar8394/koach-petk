# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from modulesApp.Planning import views

app_name = "planning"
urlpatterns = [

    path('func_Planning/', views.func_Planning, name='func_Planning'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('render_fihas/', views.render_fihas, name='renderfihas'),
    path('renderTablas/', views.renderTablas, name='renderTablas'),
    path('testfi/', views.testfi, name='testfi'),
    path('guardarFicha/', views.guardarFicha, name='guardarFicha'),
    path('eliminarFicha/', views.eliminarFicha, name='eliminarFicha'),
    path('moverFicha/', views.moverFicha, name='moverFicha'),
    path('mostrarFicha/', views.mostrarFicha, name='mostrarFicha'),
    path('fichaPersonal/<int:idFicha>/', views.fichaPersonal),
    path('fichaPersonal/<int:idFicha>/<int:idUser>/', views.fichaPersonalUsuario),
    path('guardarFichaPersonal/', views.guardarFichaPersonal, name='guardarFichaPersonal'),
    path('guardarBloque/', views.guardarBloque, name='guardarBloque'),
    path('eliminarBloque/', views.eliminarBloque, name='eliminarBloque'),
    path('previsualizarBloque/<int:idFicha>/', views.previsualizarFicha),
    path('previsualizarBloque/<int:idFicha>/<int:id>/', views.previsualizarBloque),
    path('moverBloque/', views.moverBloque, name='moverBloque'),
    path('guardarAtributo/', views.guardarAtributo, name='guardarAtributo'),
    path('eliminarAtributo/', views.eliminarAtributo, name='eliminarAtributo'),
    path('moverAtributo/', views.moverAtributo, name='moverAtributo'),
    path('atributoLista/', views.atributoLista, name='atributoLista'),
    path('listaPerfiles/', views.listaPerfiles, name='listaPerfiles'),
    path('listasExternas/', views.listasExternas, name='listasExternas'),
    path('guardarListaExterna/', views.guardarListaExterna, name='guardarListaExterna'),
    path('contenidoListaExterna/', views.contenidoListaExterna, name='contenidoListaExterna'),
    path('eliminarListaExterna/', views.eliminarListaExterna, name='eliminarListaExterna'),
    path('addproceso/', views.addproceso, name='addproceso'),
    path('guardarListaExternaHijo/', views.guardarListaExternaHijo, name='guardarListaExternaHijo'),
    path('eliminarListaExternaHijo/', views.eliminarListaExternaHijo, name='eliminarListaExternaHijo'),
    
    

    # modales    
    path('modalFicha/', views.modalFicha, name='modalFicha'),
    path('modalListaBloque/', views.modalListaBloque, name='modalListaBloque'),
    path('modalBloque/', views.modalBloque, name='modalBloque'),
    path('modalAtributo/', views.modalAtributo, name='modalAtributo'),
    path('modalListaExterna/', views.modalListaExterna, name='modalListaExterna'),
    path('modalListaExternaHijo/', views.modalListaExternaHijo, name='modalListaExternaHijo'),

    # metodos
    path('validarNombreFicha/', views.validarNombreFicha, name='validarNombreFicha'),

    # filtro
    path('filtroLista/', views.filtroLista, name='filtroLista'),
    path('filtroAtributo/', views.filtroAtributo, name='filtroAtributo'),
    path('filtroElemento/', views.filtroElemento, name='filtroElemento'),
    path('filtrar/', views.filtrar, name='filtrar'),


]