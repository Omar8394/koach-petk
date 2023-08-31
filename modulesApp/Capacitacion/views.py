from itertools import filterfalse
from unicodedata import category, decimal
from django import apps
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template import loader
from django.template.loader import render_to_string
from ..App.models import ConfTablasConfiguracion,AppPublico
from ..Capacitacion.models import Estructuraprograma, capacitacion_ActSesiones_programar, capacitacion_Actividad_Sesiones, capacitacion_Actividad_leccion, capacitacion_Actividad_tareas, capacitacion_ComponentesActividades, capacitacion_EvaluacionesPreguntas, capacitacion_EvaluacionesPreguntasOpciones, capacitacion_LeccionPaginas, capacitacion_Recursos,capacitacion_componentesXestructura,componentesFormacion,capacitacion_Tag,capacitacion_TagRecurso,capacitacion_componentesPrerequisitos,EscalasEvaluaciones,capacitacion_ActividadEvaluaciones,capacitacion_EvaluacionesBloques,capacitacion_ActividadesTiempoReal,capacitacion_Examenes,capacitacion_ExamenesResultado,capacitacion_NotificacionesMensajesXactividad,capacitacion_HistoricoActividades,capacitacion_tiempoxevaluaciones
from ..Organizational_network.models import nodos_grupos,nodos_gruposIntegrantes,nodos_PlanFormacion
from ..Comunication.models import Comunication_MsjPredeterminado,Boletin_Info,Entrenamiento_Post 
import time, json
import sys
from decimal import Decimal
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from core import settings
from pathlib import Path
from django.db.models import Q
import uuid
import mimetypes
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Count, Sum, FloatField
from ..Security.models import User
from .methods import finalizar_componente,verifylast,week
import datetime
TITULOPUBLIC = {'id_nodoGrupo_Integrantes':'#', 'fk_public': 'Usuario',  'fecha_inicio': 'fecha inicio', 'ultima_actividad': 'ultima actividad'}
# Create your 
# views here.
@register.filter
def jsonsesion(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_sesion' in data :
     return data['datos_sesion'][0]['lugar']
  else:
      return ""
@register.filter
def jsonsesionfives(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_sesion' in data :
     return data['datos_sesion'][0]['key']
  else:
      return ""  
@register.filter
def jsonsesiontwo(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_sesion' in data :
     return data['datos_sesion'][0]['tema']
  else:
      return "" 
@register.filter
def jsonsesionthre(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_sesion' in data :
     return data['datos_sesion'][0]['tipo_ritmo']
  else:
      return "" 
@register.filter
def jsonsesionfour(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_sesion' in data :
     return data['datos_sesion'][0]['ritmo']
  else:
      return "" 
@register.filter  
def jsonsesionfive(datos):
    if datos==None or datos=="" or datos=={}:
       return ""
    tlf=None
    data = json.loads(datos)

  
    if data==None or data=="" or data=={}:
       return ""
    if 'datos_recurrencia' in data :
       return data['datos_recurrencia'][0]['lugar']
    else:
      return ""   
@register.filter  
def jsonsesionfi(datos):
    if datos==None or datos=="" or datos=={}:
       return ""
    tlf=None
    data = json.loads(datos)

  
    if data==None or data=="" or data=={}:
       return ""
    if 'datos_recurrencia' in data :
       return data['datos_recurrencia'][0]['Recurrencia']
    else:
      return ""
@register.filter  
def jsonsesionfisi(datos):
    if datos==None or datos=="" or datos=={}:
       return ""
    tlf=None
    data = json.loads(datos)

  
    if data==None or data=="" or data=={}:
       return ""
    if 'datos_recurrencia' in data :
       return data['datos_recurrencia'][0]['finaliza_vuelta']
    else:
      return "" 
@register.filter  
def jsonsesionseis(datos):
    if datos==None or datos=="" or datos=={}:
       return ""
    tlf=None
    data = json.loads(datos)

  
    if data==None or data=="" or data=={}:
       return ""
    if 'datos_recurrencia' in data :
       return data['datos_recurrencia'][0]['finaliza']
    else:
      return ""              
@register.filter
def hashijos(id):
    lista=[]
    has=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=id)
    
    print(has)
    return has
@register.filter
def peso(id,test):
    totales=0
    if id == "":
        return ""
    else:
      test=capacitacion_ActividadEvaluaciones.objects.get(pk=test).fk_escalasEvaluaciones.maxima_puntuacion       
      has=capacitacion_EvaluacionesBloques.objects.get(pk=id).peso 
      total=(int(test)*int(has))
      totales=(total/100)
      print(has)
    return totales
@register.filter
def preguntas(bloques):
    lista=[]
    op=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=bloques).order_by('orden')
    
    return op
@register.filter
def preguntasopciones(bloques):
    lista=[]
    preg=capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas_id=bloques)
    print(preg)
    return preg
@register.filter
def verdadero_Falso(id):
    
    preg=capacitacion_EvaluacionesPreguntasOpciones.objects.get(pk=id).respuesta_correcta
    print(preg)
    return preg
@register.filter
def initial_fecha(id): 
    init ='No iniciado'
    inicio=capacitacion_HistoricoActividades.objects.filter(fk_nodo_Grupo_integrantes_id=id)
    if inicio.exists():       
       data = json.loads(inicio.order_by('fk_componenteXestructura')[0].datos_resumen)
       if data==None or data=="" or data=={}:
          return ""
       if  'datos_resumen' in data :
            init= data['datos_resumen'][0]['fecha_ini']
       
    else:
        inicio_real=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes_id=id) 
        if inicio_real.exists():  
           init=inicio_real.order_by('fecha_realizado')[0].fecha_realizado
         
    return init  
@register.filter
def last_atv(id): 
    init ='No iniciado'
    inicio=capacitacion_HistoricoActividades.objects.filter(fk_nodo_Grupo_integrantes_id=id)
    if inicio.exists():       
       data = json.loads(inicio.order_by('-fk_componenteXestructura')[0].datos_resumen)
       if data==None or data=="" or data=={}:
          init ='No iniciado'
       if  'datos_resumen' in data :
            ultima=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes_id=id) 
            if ultima.exists(): 
               
               init=ultima.order_by('-fecha_realizado')[0].fk_componenteActividades
            else:   
               init=data['datos_resumen'][0]['ultima_Actividad']
            
       
    else:
        inicio_real=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes_id=id) 
        if inicio_real.exists():  
           init=inicio_real.order_by('-fecha_realizado')[0].fk_componenteActividades
         
    return init  
@register.filter  
def jsonhistory(datos,tipo):
    if datos==None or datos=="" or datos=={}:
       return ""
    tlf=None
    data = json.loads(datos)

  
    if data==None or data=="" or data=={}:
       return ""
    if 'datos_resumen' in data :
       return data['datos_resumen'][0][tipo]
    else:
      return ""
@register.filter  
def busca_test(pk):
    esta=None
    test=capacitacion_ActividadEvaluaciones.objects.filter(fk_componenteActividad_id=pk)
    if test.exists():
       esta=test[0].pk
    else:
        esta=None  
    return esta 
@register.filter  
def has_time(pk):
    print(pk)
    esta=False
    test=capacitacion_tiempoxevaluaciones.objects.filter(fk_evaluacion_id=pk)
    print(test)
    if test.exists():
       esta=True
    else:
        esta=False
    print(esta)      
    return esta             
@login_required(login_url="/security/login/")
def index(request):
    
    user = request.user
    rol=user.fk_rol_usuario   
    context = {}
   
    if str(rol) == "Admin"  or str(rol) == "Lider":
       html_template = (loader.get_template('gestor_index.html'))
    else:
        html_template = (loader.get_template('page-403.html'))
    return HttpResponse(html_template.render(context, request))
def getcontentprogrmas(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if request.body:
                context={}
                data = json.load(request)
                print(data)
                title=False
                lista = []
                if data["query"] == "":
                   padres = ConfTablasConfiguracion.objects.filter(valor_elemento='Categoria')
                   categorias=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=padres[0],mostrar_en_combos=1) 
                   print(categorias)    
                   context = {'categorias':categorias}             
                   html_template = loader.get_template( 'Contenido_programas.html' )
                   return HttpResponse(html_template.render(context, request))
                if data["query"] == "find":
                   print(data)
                   programas=Estructuraprograma.objects.filter(valor_elemento='Program',fk_categoria_id=data['id'])
                   if programas.exists():
                      paginator = Paginator(programas, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"]
                      context = {"page": page,"limit": limit,'programas':programas,'data':lista,'padre':data["id"]} 
                      print(context)            
                      html_template = loader.get_template( 'renderprogramas.html' )
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {'title':title} 
                      print(context)            
                      html_template = loader.get_template( 'renderprogramas.html' )
                      return HttpResponse(html_template.render(context, request))
                       
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def modalagregarcategoria(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                if data['method'] == "Create":
                   padre=ConfTablasConfiguracion.objects.get(valor_elemento='Categoria').pk
                   categoria=ConfTablasConfiguracion()
                   categoria.fk_tabla_padre_id=padre
                   categoria.tipo_elemento=0 
                   categoria.permite_cambios=1
                   categoria.valor_elemento=None
                   categoria.mostrar_en_combos=1
                   categoria.maneja_lista=0
                   categoria.desc_elemento = data["data"]["descriptionCat"]
                   categoria.save()
                   return JsonResponse({"message":"Perfect"})
            context = {}                     
            html_template = loader.get_template('modalagregarcategoria.html')
            return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def modalAddprogram(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                if data['method'] == "Editar":
                    modelo = Estructuraprograma.objects.get(pk=data["id"])    
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Categoria")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('modalAddProgram.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Delete":
                     programa = Estructuraprograma.objects.get(pk=data["id"])
                       
                     programa.delete()
                     return JsonResponse({"message":"Deleted"}) 
                elif data["method"] == "Update":
                   programa = Estructuraprograma.objects.get(pk=data["id"])
                elif data['method'] == "Create":
                   programa=Estructuraprograma()
                   programa.fk_estructura_padre=None
                   programa.valor_elemento="Program"
                programa.descripcion=data['data']['resumenProgram']    
                programa.url=data['data']['urlProgram']
                programa.fk_categoria_id=data['data']['categoryProgram']
                programa.Titulo=data['data']['descriptionProgram']
                programa.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                 
                programa.save()
                return JsonResponse({"message":"ok"})
            
                
                                  
            categorias = ConfTablasConfiguracion.obtenerHijos(valor="Categoria")
            context = {"categorias": categorias}
            html_template = (loader.get_template('modalAddprogram.html'))
            return HttpResponse(html_template.render(context, request))
                       
            
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def Addproceso(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title=False
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                lista=[]
                if data['query'] == "":
                   procesos=Estructuraprograma.objects.filter(fk_estructura_padre_id=data['id'],valor_elemento="Process")
                   antesesor=Estructuraprograma.objects.get(pk=data['id'],valor_elemento="Program")
                   print(data)
                   if procesos.exists():
                      paginator = Paginator(procesos, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"]
                      context = {"titulo": antesesor.Titulo,"page": page,"limit": limit,'procesos':procesos,'padre':data['id'],'data':lista}
                      #print(context)
                      html_template = (loader.get_template('renderizadopro.html'))
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"titulo": antesesor.Titulo,'title':title,'padre':data['id']}
                      print(procesos)
                      html_template = (loader.get_template('renderizadopro.html'))
                      return HttpResponse(html_template.render(context, request))
            context = {}
            html_template = (loader.get_template('renderizadopro.html'))
            return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)    
def modalAddproceso(request):
    if request.method == "POST":
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title=False
        try:
            if request.body:    
                data = json.load(request)
                print(data)
            
                if data["method"] == "Delete":
                    prose = Estructuraprograma.objects.get(pk=data["id"])
                    prose.delete()
                    return JsonResponse({"message":"Deleted"}) 
                elif data['method'] == "Editar":
                    modelo = Estructuraprograma.objects.get(pk=data["id"])    
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Categoria")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('modaladdproseso.html'))
                    return HttpResponse(html_template.render(context, request)) 
                   
                elif data['method'] == "Create":
                   proAdd=Estructuraprograma.objects.get(pk=data['id']).fk_categoria_id
                   print(proAdd)
                   pro=Estructuraprograma()
                   pro.fk_estructura_padre_id=data['id']
                   pro.valor_elemento="Process"
                   pro.descripcion=data['data']['resumenProgram']    
                   pro.url=data['data']['urlProgram']
                   pro.fk_categoria_id=proAdd
                   pro.Titulo=data['data']['descriptionProgram']
                   pro.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                   pro.save()
                   return JsonResponse({"message":"ok"})
            context = {}
            html_template = (loader.get_template('modaladdproseso.html'))
            return HttpResponse(html_template.render(context, request))     
                   
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/security/login/") 
def indextwo(request,velemento,url,idActividad):
    id=idActividad
    urls=url
    elemento=velemento
    context = {'id':id,'url':urls,'elemento':elemento}
    #print(context)
    html_template = (loader.get_template('gestor_indetwo.html'))
    
    return HttpResponse(html_template.render(context, request))
def getcontentunits(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                lista=[]
                if data["query"] == "":
                   print(data['urls']) 
                   units=Estructuraprograma.objects.filter(fk_estructura_padre_id=data['pk'],url=data['urls'],valor_elemento="Module")
                   antesesor=Estructuraprograma.objects.get(pk=data['pk'],valor_elemento=data["valor"],url=data['urls'])
                   print(antesesor.Titulo)
                   if units.exists(): 
                      paginator = Paginator(units, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"]
                      context = {"titulo":antesesor.Titulo,"page": page,"limit": limit,'units':units,'pk':data['pk'],'padre':data['pk'],'data':lista}             
                      html_template = loader.get_template( 'contenidounidades.html' )
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"titulo":antesesor.Titulo,'title':title,'pk':data['pk']}             
                      html_template = loader.get_template( 'contenidounidades.html' )
                      return HttpResponse(html_template.render(context, request)) 
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
def modalAddmodulos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                if data['method'] == "Editar":
                    modelo = Estructuraprograma.objects.get(pk=data["id"])    
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Categoria")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('modalAddmodulos.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Delete":
                    unidad = Estructuraprograma.objects.get(pk=data["id"])
                    unidad.delete()
                    return JsonResponse({"message":"Deleted"})
                elif data["method"] == "Update":
                     unit = Estructuraprograma.objects.get(pk=data["id"])
                elif data['method'] == "Create":
                   proAdd=Estructuraprograma.objects.get(pk=data['id']).fk_categoria_id
                   print(proAdd)
                   unit=Estructuraprograma()
                   unit.fk_estructura_padre_id=data['id']
                   unit.fk_categoria_id=proAdd
                   unit.valor_elemento="Module"
                unit.descripcion=data['data']['resumenProgram']    
                unit.url=data['data']['urlProgram']
                   
                unit.Titulo=data['data']['descriptionProgram']
                unit.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                unit.save()
                return JsonResponse({"message":"ok"})
            
            context = {}
            html_template = (loader.get_template('modalAddmodulos.html'))
            return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getcontentcursos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                lista=[]
                if data["query"] == "":
                   cursos=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=data['id'])
                   antesesor=Estructuraprograma.objects.get(pk=data['id'])
                   print(antesesor.Titulo)
                   if cursos.exists():
                      paginator = Paginator(cursos, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"] 
                      context = {"titulo":antesesor.Titulo ,"page": page,"limit": limit,'cursos':cursos,'pk':data['id'],'padre':data['id'],'data':lista}             
                      html_template = loader.get_template( 'renderizarcursos.html' )
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"titulo":antesesor.Titulo ,'title':title,'pk':data['id']}             
                      html_template = loader.get_template( 'renderizarcursos.html' )
                      return HttpResponse(html_template.render(context, request)) 
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def modalAddcursos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                
                print(data)
                if data['method'] == "Editar":
                    modelo = componentesFormacion.objects.get(pk=data["id"])    
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('modaladdcursos.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Delete":
                    rel=capacitacion_componentesXestructura.objects.get(fk_estructuraprogramas_id=data["padre"],fk_componetesformacion=data["id"])
                    rel.fk_estructuraprogramas=Estructuraprograma.objects.get(fk_categoria__valor_elemento="Categoria_papelera")
                    rel.save()
                    # cursos = Capacitacion_componentesFormacion.objects.get(pk=data["id"])   
                    # cursos.delete()
                    return JsonResponse({"message":"Deleted"}) 
                elif data["method"] == "Update":
                   cursos = componentesFormacion.objects.get(pk=data["id"])
                   cursos.descripcion=data['data']['resumenProgram']    
                   cursos.url=data['data']['urlProgram']         
                   cursos.titulo=data['data']['descriptionProgram']
                   cursos.creditos_peso=Decimal(data['data']['creditos'].replace(',','.'))
                   cursos.Fecha_activo=data['data']['disponibleCourse']
                   #cursos.Condicion=data['data']['Condicion']
                   #cursos.tipo_ritmo_id=data['data']['categoryProgram']
                   #cursos.ritmo=data['data']['Ritmo']
                   cursos.anno_semestre=data['data']['Semestre']
                   
                   if 'checkDurationCB' in data['data']:
                      cursos.status_componente=1
                   else:
                      cursos.status_componente=0
                   if 'checkDurationC' in data['data']:
                      cursos.tiene_certificad=1
                      cursos.path_plantilla_certificado=data['data']['imagen']
                   else:
                      cursos.tiene_certificad=0
                
                   cursos.save()
                elif data['method'] == "Create":
                   
                   print(data)
                   cursos=componentesFormacion()
                   relacion=capacitacion_componentesXestructura() 
                   relacion.fk_estructuraprogramas_id=data['id']
                  
                   cursos.codigo_componente="Components"
                   cursos.descripcion=data['data']['resumenProgram']    
                   cursos.url=data['data']['urlProgram']         
                   cursos.titulo=data['data']['descriptionProgram']
                   cursos.creditos_peso=Decimal(data['data']['creditos'].replace(',','.'))
                   cursos.orden_presentacion=len(componentesFormacion.objects.all()) + 1
                   cursos.Fecha_activo=data['data']['disponibleCourse']
                   #cursos.Condicion=data['data']['Condicion']
                  # cursos.tipo_ritmo_id=data['data']['categoryProgram']
                   #cursos.ritmo=data['data']['Ritmo']
                   cursos.anno_semestre=data['data']['Semestre']
                  
                   if 'checkDurationCB' in data['data']:
                      cursos.status_componente=1
                   else:
                      cursos.status_componente=0
                   if 'checkDurationC' in data['data']:
                      cursos.tiene_certificad=1
                      cursos.path_plantilla_certificado=data['data']['imagen']
                   else:
                      cursos.tiene_certificad=0
                
                   cursos.save()
                   relacion.fk_componetesformacion=cursos
                   relacion.save()
                   
               
                
                return JsonResponse({"message":"ok"})
            categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")  
            context = {"categorias": categorias}             
            html_template = loader.get_template( 'modaladdcursos.html' )
            return HttpResponse(html_template.render(context, request)) 
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/security/login/")
def relation_componente(request):
    id=request.GET.get('id')
    Estructura=Estructuraprograma.objects.all()
    dest=Estructuraprograma.objects.get(pk=id).Titulo
    componentes=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=id)
    context = {"Estructura":Estructura,"dest":dest,"id":id ,"componentes":componentes}
    
    html_template = (loader.get_template('relation_componente.html'))
    
    return HttpResponse(html_template.render(context, request))
def update_estrutura(request) :  
    estructura=request.POST.get('estructura') 
    id=request.POST.get('id')
    notsave=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=estructura,fk_componetesformacion_id=id)
    if notsave.exists():
       return JsonResponse({"message":"no"})
    else:
       componente=capacitacion_componentesXestructura()
       componente.fk_estructuraprogramas_id=estructura
       componente.fk_componetesformacion_id=id
       componente.save()
       return JsonResponse({"message":"ok"})
def getcomponentsxestructura(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                title=False
                if data["query"] == "": 
                   componentes=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=data["id"])
                   if componentes.exists():
                      context = {"componentes":componentes}
                      html_template = (loader.get_template('rendercompxestructura.html')) 
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"title":title
                                 }
                      html_template = (loader.get_template('rendercompxestructura.html')) 
                      return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
def createactividades(request,velemento,url,idActividad):
    user = request.user
    rol=user.fk_rol_usuario 
    id=idActividad
    urls=url
    elemento=velemento
    title='Vacio'
    publico=AppPublico.objects.get(user_id=user) 
    titulo=componentesFormacion.objects.filter(codigo_componente=elemento,pk=id,url=urls)
    if titulo.exists():
        title=titulo[0].titulo
    grupos=nodos_grupos.objects.filter(fk_liderGrupo=publico,status_grupo=60) 
    print(grupos)                    
    context = {"id":id,"grupos":grupos,'url':urls,'elemento':elemento,'titulo':title}
    html_template = (loader.get_template('createactividades.html'))
    return HttpResponse(html_template.render(context, request))
def renderactividades(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["query"] == "":
                    actividad=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'],url=data['urls']).order_by('orden_presentacion')
                    print(actividad)
                    if actividad.exists():
                       context = {"actividad":actividad,'padre':data['id']}
                       html_template = (loader.get_template('renderactividade.html'))
                       return HttpResponse(html_template.render(context, request))
                    else:
                      title=True 
                      context = {"title":title,'padre':data['id']}
                      html_template = (loader.get_template('renderactividade.html'))
                      return HttpResponse(html_template.render(context, request))
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getModalChooseActivities(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                   data = json.load(request)
                   print(data)
                   if data["method"] == "Show": 
                      context = {"id":data['id']}                
                      html_template = (loader.get_template('modalchooseactividad.html'))
                      return HttpResponse(html_template.render(context, request))
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)


def getModalNewLesson(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                    tipo = ConfTablasConfiguracion.obtenerHijos(valor="Tipo_Componente")
                    print(data)
                    if data['method'] == "Edit":
                        modelo = capacitacion_ComponentesActividades.objects.get(pk=data["id"])    
                        categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                        context = {"categorias": categorias, "modelo": modelo,"status":status,"tipo":tipo}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Show":
                        context = {"status":status,"tipo":tipo}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "sort":
                        print(data)
                        paginas=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])
                        i = 1
                        for d in data['data']:
                            if d != None:
                               pagina = paginas.get(id_componenteActividades=d)
                               pagina.orden_presentacion = i
                               i = i + 1
                               pagina.save()
                        return JsonResponse({"message":"ok"}, status=200)
                    elif data["method"] == "Delete":
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        actividad.fk_componenteformacion= componentesFormacion.objects.get(codigo_componente="papelera")
                        actividad.save()
                        leccion=capacitacion_Actividad_leccion.objects.get(fk_componenteActividad_id=data["id"])
                        leccion.fk_componenteActividad=capacitacion_ComponentesActividades.objects.get(valor_elemento="papelera")
                        leccion.save()
                        return JsonResponse({"message":"Deleted"}) 
                    elif data["method"] == "Update":
                        print(data)
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        leccion=capacitacion_Actividad_leccion.objects.get(fk_componenteActividad_id=data["id"])
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                        actividad.valor_elemento='Actividad_leccion'
                        actividad.url=data['data']['urlActivity'] 
                       #actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id']))
                        #actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        leccion.titulo=data['data']['descriptionActivity']
                        leccion.descripcion=data['data']['resumenActivity']
                        leccion.fecha_disponibilidad=data['data']['disponibleLesson']
                        leccion.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                        leccion.orden_presentacion=len(capacitacion_Actividad_leccion.objects.all())
                        leccion.url=data['data']['urlActivity']
                        leccion.valor_elemento="Leccion"
                        leccion.fk_statusleccion_id=data['data']['estatusLesson']
                        leccion.save()
                        print(data)
                        return JsonResponse({"message":"ok"})
                    elif data["method"] == "Create":
                        actividad=capacitacion_ComponentesActividades()
                        leccion=capacitacion_Actividad_leccion()
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=data['data']['creditos']
                        actividad.valor_elemento='Actividad_leccion'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])) + 1
                        actividad.fk_componenteformacion_id=data['id']
                        actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        leccion.titulo=data['data']['descriptionActivity']
                        leccion.descripcion=data['data']['resumenActivity']
                        leccion.fecha_disponibilidad=data['data']['disponibleLesson']
                        leccion.peso_creditos=data['data']['creditos']
                        leccion.orden_presentacion=len(capacitacion_Actividad_leccion.objects.all()) + 1
                        leccion.url=data['data']['urlActivity']
                        leccion.valor_elemento="Leccion"
                        leccion.fk_statusleccion_id=data['data']['estatusLesson']
                        leccion.fk_componenteActividad=actividad
                        leccion.save()
                        print(data)
                        return JsonResponse({"message":"ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getModalNewtest(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                    tipo = ConfTablasConfiguracion.obtenerHijos(valor="Tipo_Componente")
                    print(data)
                   
                    if data["method"] == "Show":
                        context = {"status":status,"tipo":tipo}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        actividad.fk_componenteformacion= componentesFormacion.objects.get(codigo_componente="papelera")
                        actividad.save()
                        test=capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=data["id"])
                        test.fk_componenteActividad=capacitacion_ComponentesActividades.objects.get(valor_elemento="papelera")
                        test.save()
                        return JsonResponse({"message":"Deleted"}) 
                    elif data['method'] == "Edit":
                        print(data)
                        modelo = capacitacion_ComponentesActividades.objects.get(pk=data["id"])    
                        categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                        test= capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=data['id'])
                        context = {"categorias": categorias, "modelo": modelo,"status":status,"tipo":tipo}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "sort":
                        print(data)
                        paginas=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])
                        i = 1
                        for d in data['data']:
                            if d != None:
                               pagina = paginas.get(id_componenteActividades=d)
                               pagina.orden_presentacion = i
                               i = i + 1
                               pagina.save()
                        return JsonResponse({"message":"ok"}, status=200)
                    elif data["method"] == "Update":
                        print(data)
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        test= capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=data["id"])
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                        #actividad.valor_elemento='Actividad_leccion'
                        actividad.url=data['data']['urlActivity'] 
                       #actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id']))
                        #actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        test.calificacion_aprobar=Decimal(data['data']['minApptest'].replace(',','.')) 
                        test.duracion=data['data']['Duracion_repeats']                        
                        test.fk_escalasEvaluaciones_id=data['data']['qualificationtest']
                        test.fk_tipoduracion_id=data['data']['duration']
                        test.enviar_mensaje=data['data']['modalidad_estudiante']
                        test.enviar_notificacion_lider=data['data']['modalidad_lider']
                        test.nro_repeticiones=data['data']['repeatstest']
                        test.point_in_use=Decimal(data['data']['point_use'].replace(',','.')) 
                        test.titulo_evaluacion=data['data']['descriptionActivity']
                        test.save()
                        print(data)
                        return JsonResponse({"message":"ok"})
                    elif data["method"] == "Create": 
                        print(data)
                        test=capacitacion_ActividadEvaluaciones()
                        actividad=capacitacion_ComponentesActividades()
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=data['data']['creditos']
                        actividad.valor_elemento='Actividad_Test'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])) + 1
                        actividad.fk_componenteformacion_id=data['id']
                        actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        test.calificacion_aprobar=data['data']['minApptest'] 
                        test.duracion=data['data']['Duracion_repeats']
                        test.fk_componenteActividad=actividad
                        test.fk_escalasEvaluaciones_id=data['data']['qualificationtest']
                        test.fk_tipoduracion_id=data['data']['duration']
                        test.enviar_mensaje=data['data']['modalidad_estudiante']
                        test.enviar_notificacion_lider=data['data']['modalidad_lider']
                        test.nro_repeticiones=data['data']['repeatstest']
                        test.point_in_use=data['data']['point_use']
                        test.titulo_evaluacion=data['data']['descriptionActivity']
                        test.save()                       
                        return JsonResponse({"message":"ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)  
def renderModalNewTest(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                        data = json.load(request)
                        tipoDuracion = ConfTablasConfiguracion.obtenerHijos(valor="Tipo_Duracion")
                        escalas = EscalasEvaluaciones.objects.all()
                        
                        print('hola')
                        print(tipoDuracion)
                        if data["method"] == "Show":
                            print(data)
                            context = {"escalas":escalas, "tipoDuracion":tipoDuracion}
                            html_template = (loader.get_template('modalAddTest.html'))
                            return HttpResponse(html_template.render(context, request))
                        elif data["method"] == "Edit": 
                            test= capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=data['ids'])
                            context = {"escalas":escalas,"test":test, "tipoDuracion":tipoDuracion}
                            html_template = (loader.get_template('modalAddTest.html'))
                            return HttpResponse(html_template.render(context, request))                   
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def pageslessons(request):
    id=request.GET.get('id')
    actividad=capacitacion_ComponentesActividades.objects.get(pk=id).titulo
    lessiones=capacitacion_Actividad_leccion.objects.get(fk_componenteActividad_id=id)
    context = {'actividad':actividad,'id':lessiones.pk}
    html_template = (loader.get_template('pageslessons.html'))
    return HttpResponse(html_template.render(context, request))
def savepages(request): 
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          context = {}
          modelo = {}
          try:
            if request.body:
               data = json.load(request)
               
               path=""
               tipo="Tipo_texto"
               if data["method"] == "Create":
                  print(data)            
                  for item in data['data']['recursos']: 
                      if item != "" :
                         tipo=item['type'] 
                         path=item['path']
                      else:
                         
                         path="" 
                  print(tipo)
                  if path != "":
                     pk= capacitacion_Recursos.objects.get(path_rutas=path).pk
                  else:
                     pk=None
                  paginas=capacitacion_LeccionPaginas()
                  paginas.titulo=data['data']['minApp']
                  paginas.contenido = None
                  if data["data"]["summernote"] != "<p><br></p>":
                     paginas.contenido = data["data"]["summernote"]
                  paginas.fk_actividadLeccion_id=data['id']
                  paginas.fk_tipoContenido= ConfTablasConfiguracion.obtenerHijos("Tipo_Contenido").get(valor_elemento=tipo)
                  paginas.orden_presentacion=len(capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=data['id'])) + 1
                  paginas.fk_statusPagina=ConfTablasConfiguracion.obtenerHijos("Status_global").get(valor_elemento="Status_activo")
                  paginas.id_recursos=pk
                  paginas.save()
                  return JsonResponse({"message":"ok"}, status=200)
               elif data["method"] == "Delete":
                    paginas=capacitacion_LeccionPaginas.objects.get(pk=data['id'])
                    paginas.fk_actividadLeccion=capacitacion_Actividad_leccion.objects.get(valor_elemento="papelera")
                    paginas.save()
                    pag=capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=data['padre'], orden_presentacion__gte=paginas.orden_presentacion)
                    for pg in pag:
    
                        pg.orden_presentacion = pg.orden_presentacion - 1
                        pg.save()
                        
                    return JsonResponse({"message":"delete"}, status=200)
               elif data["method"] == "sort":
                    print(data)
                    paginas=capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=data['id'])
                    i = 1
                    for d in data['data']:
                        if d != None:
                           pagina = paginas.get(id_leccionPaginas=d)
                           pagina.orden_presentacion = i
                           i = i + 1
                           pagina.save()
                    return JsonResponse({"message":"ok"}, status=200)
               elif data["method"] == "Edit":
                    print(data)            
                    for item in data['data']['recursos']: 
                        if item != "" :
                           tipo=item['type'] 
                           path=item['path']
                        else:
                         
                           path="" 
                    print(data)
                    if path != "":
                      pk= capacitacion_Recursos.objects.get(path_rutas=path).pk
                    else:
                      pk=None
                    paginas=capacitacion_LeccionPaginas.objects.get(pk=data['id'])
                    paginas.titulo=data['data']['minApp']
                    paginas.contenido = None
                    if data["data"]["summernote"] != "<p><br></p>":
                       paginas.contenido = data["data"]["summernote"]
                    paginas.fk_tipoContenido= ConfTablasConfiguracion.obtenerHijos("Tipo_Contenido").get(valor_elemento=tipo)
                    paginas.id_recursos=pk
                    paginas.fk_statusPagina_id=data['data']['Status']
                    paginas.save()
                    return JsonResponse({"message":"ok"}, status=200)
          except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
    html_template = (loader.get_template('modalpdflessons.html'))
    return HttpResponse(html_template.render({}, request))
@login_required(login_url="/login/")
def getModalResourcesBank(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            # try:
            if request.headers.get("idPagina"):
                #Handle the files upload
                idPagina = request.headers.get('idPagina')
                myfiles = list(request.FILES.values())
                print(myfiles)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                print(fs)
                recursos = []
                for file in myfiles:
                    resourceType = mimetypes.guess_type(file.name)[0]
                    nombreImagen = str(uuid.uuid4())
                    extensionFile=Path(file.name).suffix
                    nombreImagen="res_"+nombreImagen+extensionFile
                    Ruta=settings.MEDIA_ROOT
                    print(Ruta)
                    # folder = request.path.replace("/", "_")
                    try:
                        os.mkdir(os.path.join(Ruta))
                    except:
                        pass
                    #save file
                    fs.save(Ruta+'/'+nombreImagen, file)
                    #after save file lets go to save on BBDD
                    newRecurso = capacitacion_Recursos()
                    newRecurso.path_rutas = nombreImagen
                    if "application/pdf" in resourceType:
                        print("hola")
                        resourceType = "Tipo_pdf"
                    if "image/" in resourceType:
                        resourceType = "Tipo_imagen"
                    if "audio/" in resourceType:
                        resourceType = "Tipo_audio"
                    newRecurso.fk_tipoRecurso = ConfTablasConfiguracion.obtenerHijos("Tipo_Contenido").get(valor_elemento=resourceType)
                    # newRecurso.fk_publico_autor = request.user.extensionusuario.Publico
                    tags = request.POST.get("tagResource")
                    if "," in tags:
                         tags = tags.split(",")
                    else:
                         tags = [tags]
                    newRecurso.save()
                    for newtag in tags:
                        tag = capacitacion_Tag.objects.filter(desc_tag=newtag)
                        if tag.exists():
                             tag_recurso = capacitacion_TagRecurso(fk_tag=tag[0], fk_recurso=newRecurso)
                             tag_recurso.save()
                        else:
                             tag = capacitacion_Tag(desc_tag=newtag)
                             tag.save()
                             tag_recurso = capacitacion_TagRecurso(fk_tag=tag, fk_recurso=newRecurso)
                             tag_recurso.save()
                    # #add resources
                    recursos.append({"id":newRecurso.pk, "path":newRecurso.path_rutas, "type":resourceType})
                return JsonResponse({"message":"Perfect", "recursos":recursos})
            else:
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    #nananananananana batmannnn
                    recursos = capacitacion_Recursos.objects.all() 
                    recursos = recursos.order_by('-id_recurso')[:10]
                    tags = capacitacion_Tag.objects.all().order_by('desc_tag')
                    context["recursos"] = recursos
                    context["tags"] = tags
                    print(context)
                    html_template = (loader.get_template('modalBancoRecursos.html'))
                    return HttpResponse(html_template.render(context, request))
                # elif data["method"] == "Find":
                #     modelo = Paginas.objects.get(pk=data["id"])
                #     context = {"modelo": modelo}
                #     html_template = (loader.get_template('components/modalAddPagina.html'))
                #     return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Create":
                    recurso = capacitacion_Recursos.objects.filter(path_rutas=data["data"]["path"])
                    if recurso.exists():
                        return JsonResponse({"message":"Already exists", "id":recurso[0].pk, "path":recurso[0].path})
                    else:
                        newRecurso = capacitacion_Recursos()
                       
                        newRecurso.path_rutas = data["data"]["path"]
                       
                        
                        newRecurso.fk_tipoRecurso = ConfTablasConfiguracion.obtenerHijos("Tipo_Contenido").get(valor_elemento=data["data"]["tipo_recurso"])
                        
                        tags = data["data"]["tags"]
                        if "," in tags:
                            tags = tags.split(",")
                        else:
                            tags = [tags]
                        newRecurso.save()
                        for newtag in tags:
                            tag = capacitacion_Tag.objects.filter(desc_tag=newtag)
                            if tag.exists():
                                tag_recurso = capacitacion_TagRecurso(fk_tag=tag[0], fk_recurso=newRecurso)
                                tag_recurso.save()
                            else:
                                tag = capacitacion_Tag(desc_tag=newtag)
                                tag.save()
                                tag_recurso = capacitacion_TagRecurso(fk_tag=tag, fk_recurso=newRecurso)
                                tag_recurso.save()
                        return JsonResponse({"message":"Perfect", "id":newRecurso.pk, "path":newRecurso.path_rutas, "type":"Tipo_video"})
                
            # except:
            #     return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def getContentRecursos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            if request.body:
                data = json.load(request)
                if data["show"] == "tags":
                    if data["query"] == "" or data["query"] == None:
                        lista = capacitacion_Tag.objects.all().order_by("desc_tag")
                    else:
                        lista = capacitacion_Tag.objects.filter(desc_tag__icontains=data["query"]).order_by("desc_tag")
                if data["show"] == "resources":
                    tag = capacitacion_Tag.objects.get(pk=data["tag"])
                    lista = capacitacion_TagRecurso.objects.filter(fk_tag=tag)
                context = {"data":lista, "show":data["show"]}
                html_template = (loader.get_template('contenidoRecursos.html'))
                return HttpResponse(html_template.render(context, request))
def renderpaginas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                modelo = {}
                title=False
                data = json.load(request)
                print(data)
                if data["query"] == "":
                    actividad=capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=data['id']).order_by('orden_presentacion')
                    status=ConfTablasConfiguracion.obtenerHijos("Status_global")
                    print(actividad)
                    if actividad.exists():
                       context = {"status":status,"actividad":actividad,'padre':data['id']}
                       html_template = (loader.get_template('renderpaginas.html'))
                       return HttpResponse(html_template.render(context, request))
                    else:
                      title=True 
                      context = {"title":title,'padre':data['id']}
                      html_template = (loader.get_template('renderpaginas.html'))
                      return HttpResponse(html_template.render(context, request))
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def previewlessons(request):
    id=request.GET.get('id')  
    paginas=capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=id).order_by('orden_presentacion')
    context = {'paginas':paginas}
    html_template = (loader.get_template('previewpages.html'))
    return HttpResponse(html_template.render(context, request))
def preRequirements(request):
    result=Estructuraprograma.objects.filter(valor_elemento="Program") 
    context = {'result':result}
    html_template = (loader.get_template('prerequisitos.html'))
    return HttpResponse(html_template.render(context, request))
def comboboxpro(request):
    
    valor=request.GET.get('valor')
    tipo=request.GET.get('tipo')
    post=request.GET.get('edita_post' or None)
    edita=''
    print(post)
    if post is not None:
       edita=Entrenamiento_Post.objects.get(pk=post) 
       
    hay=False
    print(valor)
    print(tipo)
    if tipo == "componente":
        hay=1
    elif tipo == "atv":
        hay=2    
    data = {'opsion2': metodo_llenar_combo(valor,tipo),'hay':hay,'edita':edita}
    print(data)
    html_template = (loader.get_template('comboboxpro.html'))
    return HttpResponse(html_template.render(data, request))
def metodo_llenar_combo(valor,tipo):
    valor1=valor
    tipo2=tipo
    if tipo2 == "pro":
       result1=Estructuraprograma.objects.filter(fk_estructura_padre_id=valor1,valor_elemento="Process")
       print(result1)
       lista=[]

       for file in result1:
        
           lista.append(file)
       print(lista)    
       return lista
    elif tipo2 =="modulos":
       result1=Estructuraprograma.objects.filter(fk_estructura_padre_id=valor1,valor_elemento="Module")
       print(result1)
       lista=[]

       for file in result1:
        
           lista.append(file)
       print(lista)    
       return lista
    elif tipo2 == "componente":
       result1=capacitacion_componentesXestructura.objects.filter(fk_estructuraprogramas_id=valor1)
       print(result1)
       lista=[]

       for file in result1:
        
           lista.append(file)
       print(lista)    
       return lista
    elif tipo2 == "atv":
       result1=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=valor1)
       print(result1)
       lista=[]

       for file in result1:
        
           lista.append(file)
       print(lista)    
       return lista
def renderListasPublic(request):
    
    id = request.POST.get('id', None)
    tipo = request.POST.get('tipo', None)
    tipoHijo = request.POST.get('tipoHijo', None)
    tipoPadre = request.POST.get('tipoPadre', None)
    req = None
    #print(id)
    #print(tipo)
    #print(tipoHijo)
    #print(tipoPadre)
    
        
    if (tipo == 'Estructuraprograma'):

         if tipoPadre: 

              structuras=capacitacion_ComponentesActividades.objects.all()
              structuras=structuras.filter(fk_componenteformacion_id=tipoPadre)
              structuras=structuras.exclude(id_componenteActividades=tipoHijo)
              #print(structuras)
              
              actividad = capacitacion_ComponentesActividades.objects.get(pk=tipoHijo)
              #print(actividad)
              requisitos=capacitacion_componentesPrerequisitos.objects.filter(fk_componenteActividades=actividad)
              prerequisitos=capacitacion_componentesPrerequisitos.objects.filter(fk_prerequisito=actividad)
              for x in requisitos:
                  structuras=structuras.exclude(id_componenteActividades=x.fk_componenteActividades.id_componenteActividades)
                  print(structuras)
              for x in prerequisitos:
                  structuras=structuras.exclude(id_componenteActividades=x.fk_prerequisito.id_componenteActividades)
                  print(structuras)
              if(structuras.first()): print(structuras.first().valor_elemento)
              html = render_to_string('listaspre.html', {'lista': structuras, 'tipo': 'Estructuraprograma'})
              req = render_to_string('listaspre.html', {'lista': requisitos, 'tipo': 'cursos_prerequisitos'})
              
   
    response = {

         'competence': html,
         'requirements': req if req else None

    }

    return JsonResponse(response)
def requirementos(request):  


    if request.method == "POST":  
        
        tipo = request.POST.get('tipo')
        requisito = capacitacion_ComponentesActividades.objects.get(id_componenteActividades=request.POST.get('requisito'))
        actividad = capacitacion_ComponentesActividades.objects.get(id_componenteActividades=request.POST.get('actividad'))
        #actividad=request.POST.get('actividad')
        if tipo == 'agregar':
            matricula=capacitacion_componentesPrerequisitos.objects.create(fk_componenteActividades=actividad,fk_prerequisito=requisito)
            matricula.save()

        else:
            matricula = capacitacion_componentesPrerequisitos.objects.get(fk_componenteActividades=actividad,fk_prerequisito=requisito)
            matricula.delete()  

        return JsonResponse({'mensaje': 'succes'})

    return JsonResponse({})   
def getModalNewhomework(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                    if data["method"] == "Show":
                       context = {"status":status,"categorias":categorias}
                       html_template = (loader.get_template('modalAddLesson.html'))
                       return HttpResponse(html_template.render(context, request))
                    elif data['method'] == "Edit":
                        print(data)
                        modelo = capacitacion_ComponentesActividades.objects.get(pk=data["id"]) 
                        tareas= capacitacion_Actividad_tareas.objects.get(fk_componenteActividad_id=data["id"])   
                        categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                        context = {"categorias": categorias, "modelo": modelo,"status":status,"tareas":tareas}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Update":
                        print(data)
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        tareas=capacitacion_Actividad_tareas.objects.get(fk_componenteActividad_id=data["id"])
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                        actividad.valor_elemento='Actividad_Tarea'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        tareas.Descripcion_tarea=data['data']['resumenActivity']
                        tareas.titulo=data['data']['descriptionActivity']
                        tareas.fk_status_id=data['data']['estatusLesson']
                        tareas.fk_tipoTiempoEntrega_id=data['data']['tipo_ritmo']
                        tareas.path_recurso=data['data']['summernote']
                        tareas.tiempo_entrega=data['data']['ritmo_entrega']
                        tareas.save()
                        return JsonResponse({"message":"ok"})
                    elif data["method"] == "Delete":
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        actividad.fk_componenteformacion= componentesFormacion.objects.get(codigo_componente="papelera")
                        actividad.save()
                        tarea=capacitacion_Actividad_tareas.objects.get(fk_componenteActividad_id=data["id"])
                        tarea.fk_componenteActividad=capacitacion_ComponentesActividades.objects.get(valor_elemento="papelera")
                        tarea.save()
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Create":
                        print(data)
                        actividad=capacitacion_ComponentesActividades()
                        tareas=capacitacion_Actividad_tareas()
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=data['data']['creditos']
                        actividad.valor_elemento='Actividad_Tarea'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])) + 1
                        actividad.fk_componenteformacion_id=data['id']
                        actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        tareas.Descripcion_tarea=data['data']['resumenActivity']
                        tareas.titulo=data['data']['descriptionActivity']
                        tareas.fk_componenteActividad=actividad
                        tareas.fk_status_id=data['data']['estatusLesson']
                        tareas.fk_tipoTiempoEntrega_id=data['data']['tipo_ritmo']
                        tareas.path_recurso=data['data']['summernote']
                        tareas.tiempo_entrega=data['data']['ritmo_entrega']
                        tareas.save()
                        return JsonResponse({'mensaje': 'ok'})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getModalNewsesiones(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                   
                    if data["method"] == "Show":
                       context = {"status":status}
                       html_template = (loader.get_template('modalAddLesson.html'))
                       return HttpResponse(html_template.render(context, request))           
                    elif data['method'] == "Edit":
                        print(data)
                        modelo = capacitacion_ComponentesActividades.objects.get(pk=data["id"]) 
                        tareas= capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad_id=data["id"])   
                        
                        context = {"modelo": modelo,"status":status,"tareas":tareas}
                        html_template = (loader.get_template('modalAddLesson.html'))
                        return HttpResponse(html_template.render(context, request))
                    elif data["method"] == "Delete":
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        actividad.fk_componenteformacion= componentesFormacion.objects.get(codigo_componente="papelera")
                        actividad.save()
                        sesion=capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad_id=data["id"])
                        sesion.fk_componenteActividad=capacitacion_ComponentesActividades.objects.get(valor_elemento="papelera")
                        sesion.save()
                        
                        return JsonResponse({"message":"Deleted"})
                    elif data["method"] == "Update":
                        print(data)
                        pro_sesion=None
                        actividad=capacitacion_ComponentesActividades.objects.get(pk=data["id"])
                        sesiones=capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad_id=data["id"])
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                        actividad.valor_elemento='Actividad_Sesiones'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        sesiones.Descripción=data['data']['resumenActivity']
                        sesiones.titulo=data['data']['descriptionActivity']                        
                        sesiones.fk_status_id=data['data']['estatusLesson']
                        sesiones.modalidad=data['data']['modalidades']                       
                        sesiones.save()
                        try: 
                          pro_sesion = capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones=sesiones)  
                          pro_sesion.delete()
                        except capacitacion_ActSesiones_programar.DoesNotExist:
                          pro_sesion = None  
                        return JsonResponse({"message":"ok"})
                    elif data["method"] == "Create":
                        print(data)
                        actividad=capacitacion_ComponentesActividades()
                        sesiones=capacitacion_Actividad_Sesiones()
                        actividad.titulo=data['data']['descriptionActivity']
                        actividad.descripcion=data['data']['resumenActivity']
                        actividad.fecha_disponibilidad=data['data']['disponibleLesson']
                        actividad.peso_creditos=data['data']['creditos']
                        actividad.valor_elemento='Actividad_Sesiones'
                        actividad.url=data['data']['urlActivity'] 
                        actividad.orden_presentacion=len(capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])) + 1
                        actividad.fk_componenteformacion_id=data['id']
                        actividad.fk_tipocomponente_id=ConfTablasConfiguracion.objects.get(valor_elemento=data['tipo']).pk 
                        actividad.fk_statuscomponente_id=data['data']['estatusLesson']
                        actividad.save()
                        sesiones.Descripción=data['data']['resumenActivity']
                        sesiones.titulo=data['data']['descriptionActivity']
                        sesiones.fk_componenteActividad=actividad
                        sesiones.fk_status_id=data['data']['estatusLesson']
                        sesiones.modalidad=data['data']['modalidades']
                       
                        sesiones.save()
                        return JsonResponse({'mensaje': 'ok'})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)       
def programarsesiones(request):
    id=request.GET.get('id')
    print(id)
    pro_sesion=None
    title=0
    actividad=capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad_id=id)
    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
    try: 
        pro_sesion=capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones=actividad)  
        title=1           
    except capacitacion_ActSesiones_programar.DoesNotExist:
        pro_sesion = None
        
    context = {'categorias':categorias,'padre':actividad.fk_componenteActividad.fk_componenteformacion_id,'pro_sesion':pro_sesion,'title':title,'actividad':actividad,'id':id}
    print(context)
    html_template = (loader.get_template('programarsesiones.html'))
    return HttpResponse(html_template.render(context, request))           
def rendersesiones(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                modelo = {}
                title=False
                
                data = json.load(request)
                nodos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=1)                
                ponente=AppPublico.objects.filter(user_id__fk_rol_usuario_id=110)
                usos_horarios=ConfTablasConfiguracion.obtenerHijos(valor="Zonas_horarias")
                pro_sesion=None
                categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                print(ponente)
                print(data)
                
                try: 
                   pro_sesion=capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones_id=data['id'])  
                   
                except capacitacion_ActSesiones_programar.DoesNotExist:
                   pro_sesion = None
                if data["query"] == "" and data["tipo"] == 0:                
                    context = {'categorias':categorias,'pro_sesion':pro_sesion,'nodo':nodos,'ponente':ponente}
                    html_template = (loader.get_template('rendersesionestipouno.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["query"] == "" and data["tipo"] == 1:
                    context = {'categorias':categorias,'nodo':nodos,'ponente':ponente,'pro_sesion':pro_sesion,'usos_horarios':usos_horarios}
                    html_template = (loader.get_template('rendersesiones.html'))
                    return HttpResponse(html_template.render(context, request))
                     
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)

def savesesionprogramas(request): 
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          context = {}
          modelo = {}
          try:
            if request.body:
               data = json.load(request)
               
              
               if data["method"] == "Create":
                  print(data)
                  programar=[]
                  obj={}
                  datos = {}
                  obj["lugar"]= data['data']['linkForum']
                  obj["tema"]= data['data']['idForum']                 
                  if 'keyForum' in data['data']:
                      obj["key"]=data['data']['keyForum']
                  programar.append(obj or 0)
                  datos['datos_sesion']=programar                               
                  programar=capacitacion_ActSesiones_programar() 
                  programar.fecha_inicio=data['data']['datetimeForum']
                  programar.datos_sesion=json.dumps(datos)
                  programar.fk_grupoNodo_id=data['data']['Grupo']
                  programar.director_ponente_id=data['data']['Director']
                  programar.status_sesion=ConfTablasConfiguracion.objects.get(valor_elemento="Status_activo")                   
                  programar.fecha_finalizacion=data['data']['datetimeFinal']
                  programar.id_capacitacionActividadSesiones_id=data['id']
                  programar.duracion=Decimal(data['data']['idur'].replace(',','.'))
                  programar.hora_inicio=Decimal(data['data']['hora_init'].replace(',','.'))
                  programar.gmt_horainternacional=ConfTablasConfiguracion.objects.get(pk=data['data']['uso']) 
                  if 'checkDurationC' in data['data']:
                      programartwo=[]
                      objtwo={}
                      datostwo = {}
                      objtwo["lugar"]= data['data']['categoryProgram']
                      objtwo["Recurrencia"]= data['data']['Ritmo'] 
                      if 'finalizar' in data['data']:
                          objtwo["finaliza"]=data['data']['finalizar']
                      else:
                          objtwo["finaliza"]=None    
                      if 'finalizar_vez'in data['data']: 
                          objtwo["finaliza_vuelta"]=data['data']['finalizar_vez']    
                      else:
                          objtwo["finaliza_vuelta"]=None
                      programartwo.append(objtwo or 0)
                      datostwo['datos_recurrencia']=programartwo 
                      programar.recurrente=1 
                      programar.datos_recurrencia=json.dumps(datostwo) 
                  programar.save()
                  return JsonResponse({"message":"ok"})
               elif data["method"] == "Edit":
                    programaredit=capacitacion_ActSesiones_programar.objects.get(pk=data['id'])
                    programaredit.delete()
                    programar=[]
                    obj={}
                    datos = {}
                    obj["lugar"]= data['data']['linkForum']
                    obj["tema"]= data['data']['idForum']                   
                    if 'keyForum' in data['data']:
                        obj["key"]=data['data']['keyForum']
                    programar.append(obj or 0)
                    datos['datos_sesion']=programar
                    programar=capacitacion_ActSesiones_programar() 
                    programar.fecha_inicio=data['data']['datetimeForum']
                    programar.datos_sesion=json.dumps(datos)
                    programar.fk_grupoNodo_id=data['data']['Grupo']
                    programar.director_ponente_id=data['data']['Director']
                    programar.status_sesion=ConfTablasConfiguracion.objects.get(valor_elemento="Status_activo")                   
                    programar.fecha_finalizacion=data['data']['datetimeFinal']
                    programar.id_capacitacionActividadSesiones_id=data['ed']
                    programar.duracion=Decimal(data['data']['idur'].replace(',','.'))
                    programar.hora_inicio=Decimal(data['data']['hora_init'].replace(',','.'))
                    programar.gmt_horainternacional=ConfTablasConfiguracion.objects.get(pk=data['data']['uso']) 
                    if 'checkDurationC' in data['data']:
                      programartwo=[]
                      objtwo={}
                      datostwo = {}
                      objtwo["lugar"]= data['data']['categoryProgram']
                      objtwo["Recurrencia"]= data['data']['Ritmo'] 
                      if 'finalizar' in data['data']:
                          objtwo["finaliza"]=data['data']['finalizar']
                      else:
                          objtwo["finaliza"]=None    
                      if 'finalizar_vez'in data['data']: 
                          objtwo["finaliza_vuelta"]=data['data']['finalizar_vez']    
                      else:
                          objtwo["finaliza_vuelta"]=None
                      programartwo.append(objtwo or 0)
                      datostwo['datos_recurrencia']=programartwo 
                      programar.recurrente=1 
                      programar.datos_recurrencia=json.dumps(datostwo)
                    programar.save()
                    print(data)
                    return JsonResponse({"message":"ok"})
               elif data["method"] == "Exepcion":
                   programaredit=capacitacion_ComponentesActividades.objects.get(pk=data['id'])
                   sesion=capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad=programaredit)
                   programasesion=capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones=sesion)
                  
                   print(data)
                   return JsonResponse({"message":"ok"})
          except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
def testinit(request):
    id=request.GET.get('id')
    print(id)
    test=capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=id)
    has=EscalasEvaluaciones.objects.all()
    padre=ConfTablasConfiguracion.objects.filter(valor_elemento="Tipo_Pregunta")
    tipos_pre=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=padre[0].id_tabla)
    context = {'test':test,'has':has, 'tipos_pre':tipos_pre}
    html_template = (loader.get_template('testinit.html'))
    return HttpResponse(html_template.render(context, request))
def renderrepeats(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                data = json.load(request)               
                if data["query"] == "save" : 
                    print(data)
                   
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                    context = {'categorias':categorias}
                    html_template = (loader.get_template('renderepeats.html'))
                    return HttpResponse(html_template.render(context, request)) 
                elif data["query"] == "edit":
                    pro_sesion=capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones_id=data['ids'])  
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Ritmo_Capacitacion")
                    context = {'categorias':categorias,'pro_sesion':pro_sesion}
                    html_template = (loader.get_template('renderepeats.html'))
                    return HttpResponse(html_template.render(context, request)) 
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)             
def rendertest(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                modelo = {}
                title=False
                
                data = json.load(request)
                tipo_preguntas=ConfTablasConfiguracion.obtenerHijos(valor="Tipo_Pregunta")
                if data["query"] == "" : 
                    print(data)  
                    #test=capacitacion_ActividadEvaluaciones.objects.get(pk=data['id']).fk_escalasEvaluaciones.maxima_puntuacion     
                    bloques=capacitacion_EvaluacionesBloques.objects.filter(fk_ActividadEvaluaciones_id=data['id'])             
                    if bloques.exists():
                      
                       context = {'bloques':bloques,'tipo_preguntas':tipo_preguntas}
                       html_template = (loader.get_template('rendertestbloques.html'))
                       return HttpResponse(html_template.render(context, request))
                    else:
                       title= True
                       context = {'title': title,'tipo_preguntas':tipo_preguntas}
                       html_template = (loader.get_template('rendertestbloques.html'))
                       return HttpResponse(html_template.render(context, request)) 
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def renderpreguntas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                modelo = {}
                title=False
                
                data = json.load(request)
                #tipo_preguntas=ConfTablasConfiguracion.obtenerHijos(valor="Tipo_Pregunta")
                if data["query"] == "" : 
                    print(data['pk'])
                    tipo_preguntas=ConfTablasConfiguracion.objects.get(pk=data['id']).desc_elemento     
                    if tipo_preguntas == 'Simple':
                       context={'id':data['pk'],'peso':data['peso']} 
                       html_template = (loader.get_template('renderpreguntassimple.html'))
                       return HttpResponse(html_template.render(context, request))
                    elif tipo_preguntas == 'Multiple':
                       context={'id':data['pk'],'peso':data['peso']} 
                       html_template = (loader.get_template('renderpreguntasmultiples.html'))
                       return HttpResponse(html_template.render(context, request))
                    elif tipo_preguntas == 'VoF': 
                       context={'id':data['pk'],'peso':data['peso']} 
                       html_template = (loader.get_template('renderverdaderfalso.html'))
                       return HttpResponse(html_template.render(context, request)) 
                    elif tipo_preguntas == 'Parrafo': 
                       context={'id':data['pk'],'peso':data['peso']} 
                       html_template = (loader.get_template('renderparrafo.html'))
                       return HttpResponse(html_template.render(context, request))               
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)           
def renderizarnuevaspre(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                modelo = {}
                title=False
                
                data = json.load(request)
                
                if data["query"] == "" : 
                    preguntas=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['vl']).order_by('orden')
                   
                    context={'preguntas':preguntas,'vl':data['vl']}
                    html_template = (loader.get_template('rendertapreg.html'))
                    return HttpResponse(html_template.render(context, request))
                    #return JsonResponse({'data':findpregunta}, safe=False)
                    
                      
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getModalbloques(request):            
   if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    escalas = EscalasEvaluaciones.objects.all()
                    if data["method"] == "Show":
                       print(data)
                       context = {'escalas':escalas}
                       html_template = (loader.get_template('modalAddBlock.html'))
                       return HttpResponse(html_template.render(context, request))            
                    elif data["method"] == "Create": 
                         total=0
                         
                         bloque=capacitacion_EvaluacionesBloques.objects.filter(fk_ActividadEvaluaciones_id=data["id"])     
                         for item in bloque:
                            
                             total=total+item.peso
                         print(total)
                         if total + Decimal(data['data']['blocknum'].replace(',','.')) > 100:
                            return JsonResponse({"message":"No"})
                         else: 
                           bloques=capacitacion_EvaluacionesBloques()
                           bloques.Titulo_bloque=data['data']['blockTitle']
                           bloques.instrucciones_bloque=data['data']['blockText']
                           bloques.peso=Decimal(data['data']['blocknum'].replace(',','.'))
                           bloques.tipo_bloque=data['data']['modalidad']
                           bloques.valor_elemento="block"
                           bloques.fk_escalasEvaluaciones_id=data['data']['qualificationtest']
                           bloques.fk_ActividadEvaluaciones_id=data['id']
                           bloques.save()
                           return JsonResponse({"message":"ok"})
                    elif data["method"] == "Delete":
                        actividad=capacitacion_EvaluacionesBloques.objects.get()
                        actividad.fk_ActividadEvaluaciones= capacitacion_ActividadEvaluaciones.objects.get(codigo_componente="papelera")
                        actividad.save()
                        
                    elif data["method"] == "Update": 
                         print(data)
                         bloques=capacitacion_EvaluacionesBloques.objects.get(pk=data["id"])
                         bloques.Titulo_bloque=data['data']['blockTitle']
                         bloques.instrucciones_bloque=data['data']['blockText']
                         bloques.peso=Decimal(data['data']['blocknum'].replace(',','.'))
                         bloques.tipo_bloque=data['data']['modalidad']
                         bloques.fk_escalasEvaluaciones_id=data['data']['qualificationtest']
                         bloques.save()
                         return JsonResponse({"message":"ok"})
                    elif data["method"] == "Edit":
                         bloques=capacitacion_EvaluacionesBloques.objects.get(pk=data['id'])               
                         context = {'bloques':bloques,'escalas':escalas}
                         html_template = (loader.get_template('modalAddBlock.html'))
                         return HttpResponse(html_template.render(context, request))
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                                                                      


@login_required(login_url="/login/")
def getModalNewSimple(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if data['method']=="Create":
                    total=0
                         
                    bloque=capacitacion_EvaluacionesBloques.objects.get(pk=data['fatherId'])   
                    masimapt= bloque.fk_ActividadEvaluaciones.fk_escalasEvaluaciones.maxima_puntuacion
                    testpoint=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])
                    
                    for item in testpoint:
                        total=total+item.puntos_pregunta
                    print(total)
                    portje=(bloque.peso * masimapt)/100
                    print(portje)
                    if total + Decimal(data['puntosPregunta']) > portje:
                        return JsonResponse({"message":"No"})
                    else:    
                       pregunta=capacitacion_EvaluacionesPreguntas.objects.create()
                       pregunta.fk_evaluacionesBloques_id=data['fatherId']
                       pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Simple").pk     
                       pregunta.texto_pregunta=data['textoPregunta']
                       pregunta.puntos_pregunta=data['puntosPregunta']
                       pregunta.orden=len(capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])) + 1
                       pregunta.save()
                       hijos = data["hijos"]
                       if hijos:
                          print(hijos)
                          selectetedOp=int(data['select2'])     
                          for newOpcion in hijos:
                                
                              Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                              Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                              Opcion.texto_opcion=newOpcion['OpcionText']       
                              Opcion.respuesta_correcta=True if newOpcion['id']==selectetedOp else False
                              Opcion.save()
                    
                       return JsonResponse({"message": "ok"})
                
                #return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                                                                      
@login_required(login_url="/login/")
def EditNewSimple(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if "delete" in data:
                    print(data['id'])
                    actividad=capacitacion_EvaluacionesPreguntas.objects.get(pk=data['id'])
                    print(actividad)
                    actividad.fk_evaluacionesBloques= capacitacion_EvaluacionesBloques.objects.get(valor_elemento="block_papelera")
                    actividad.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idFind"])
                    listaChilds = list(childs.values())
                    print(listaChilds)
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Update":
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    pregunta.orden=pregunta.orden
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Simple").pk
                    pregunta.save()
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
                            selectetedOp=int(data['select2'])     
                            for newOpcion in hijos:
                                
                                 Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                                 Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']   
                                    
                                 Opcion.respuesta_correcta=True if newOpcion['id']==selectetedOp else False
                                 Opcion.save()
                    
                    
                
                    return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
@login_required(login_url="/login/")
def EditNewMultiple(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if "delete" in data:
                    print(data)
                    print(data)
                    actividad=capacitacion_EvaluacionesPreguntas.objects.get(pk=data['id'])
                    actividad.fk_evaluacionesBloques= capacitacion_EvaluacionesBloques.objects.get(valor_elemento="block_papelera")
                    actividad.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idFind"])
                    listaChilds = list(childs.values())
                    print(listaChilds)
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Update":
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    pregunta.orden=pregunta.orden
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Multiple").pk
                    pregunta.save()
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
                                
                            for newOpcion in hijos:
                                
                                 Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                                 Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']                                    
                                 Opcion.porc_respuesta=float(newOpcion['value'])
                                 Opcion.save()                    
                    
                
                    return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def EditNewparrafo(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if "delete" in data:
                    print(data)
                    print(data)
                    actividad=capacitacion_EvaluacionesPreguntas.objects.get(pk=data['id'])
                    actividad.fk_evaluacionesBloques= capacitacion_EvaluacionesBloques.objects.get(valor_elemento="block_papelera")
                    actividad.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idFind"])
                    listaChilds = list(childs.values())
                    print(listaChilds)
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Update":
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    pregunta.orden=pregunta.orden
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Parrafo").pk
                    pregunta.save()
                                        
                    
                
                    return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
           
@login_required(login_url="/login/")
def EditNewtof(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if "delete" in data:
                    print(data)
                   
                    actividad=capacitacion_EvaluacionesPreguntas.objects.get(pk=data['id'])
                    actividad.fk_evaluacionesBloques= capacitacion_EvaluacionesBloques.objects.get(valor_elemento="block_papelera")
                    actividad.save()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.filter(pk=data["idFind"])
                    findpregunta = list(pregunta.values())
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idFind"])
                    listaChilds = list(childs.values())
                    print(listaChilds)
                    return JsonResponse({"data":findpregunta[0], "childs":listaChilds}, safe=False)
                
                if data["method"] == "Update":
                    pregunta=capacitacion_EvaluacionesPreguntas.objects.get(pk=data["idViejo"])
                    pregunta.orden=pregunta.orden
                    pregunta.texto_pregunta=data['textoPregunta']
                    pregunta.puntos_pregunta=data['puntosPregunta']
                    pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="VoF").pk
                    pregunta.save()
                    childs = capacitacion_EvaluacionesPreguntasOpciones.objects.filter(fk_capacitacionEvaluacionesPreguntas=data["idViejo"])
                    
                    hijos = data["hijos"]
                    if hijos:
                            print(hijos)
                        
                            if "idViejo" in data:
                                 
                                 childs.delete()
                                
                            for newOpcion in hijos:
                                
                                Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                                Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                                Opcion.texto_opcion=newOpcion['OpcionText']    
                                Opcion.porc_respuesta=float(newOpcion['value'])  
                                Opcion.respuesta_correcta=int(newOpcion['trueFalse'])  
                                Opcion.save()
                    
                
                    return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                       
@login_required(login_url="/login/")
def getModalNewparrafo(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data)
                if data['method']=="Create":
                    total=0
                         
                    bloque=capacitacion_EvaluacionesBloques.objects.get(pk=data['fatherId'])   
                    masimapt= bloque.fk_ActividadEvaluaciones.fk_escalasEvaluaciones.maxima_puntuacion
                    testpoint=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])
                    
                    for item in testpoint:
                        total=total+item.puntos_pregunta
                    print(total)
                    portje=(bloque.peso * masimapt)/100
                    print(portje)
                    if total + Decimal(data['puntosPregunta']) > portje:
                        return JsonResponse({"message":"No"})
                    else:    
                       pregunta=capacitacion_EvaluacionesPreguntas.objects.create()
                       pregunta.fk_evaluacionesBloques_id=data['fatherId']
                       pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Parrafo").pk     
                       pregunta.texto_pregunta=data['textoPregunta']
                       pregunta.puntos_pregunta=data['puntosPregunta']
                       pregunta.orden=len(capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])) + 1
                       pregunta.save()                     
                    
                       return JsonResponse({"message": "ok"})
                
                #return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                                                                                     

               


               
                
                

              

                
                        
               
@login_required(login_url="/login/")
def getModalNewMultiple(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                print(data['method'])
                if data['method']=="Create":
                    total=0
                         
                    bloque=capacitacion_EvaluacionesBloques.objects.get(pk=data['fatherId'])   
                    masimapt= bloque.fk_ActividadEvaluaciones.fk_escalasEvaluaciones.maxima_puntuacion
                    testpoint=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])
                    
                    for item in testpoint:
                        total=total+item.puntos_pregunta
                    print(total)
                    portje=(bloque.peso * masimapt)/100
                    print(portje)
                    if total + Decimal(data['puntosPregunta']) > portje:
                        return JsonResponse({"message":"No"})
                    else: 
                       pregunta=capacitacion_EvaluacionesPreguntas.objects.create()
                       pregunta.fk_evaluacionesBloques_id=data['fatherId']
                       pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="Multiple").pk     
                       pregunta.texto_pregunta=data['textoPregunta']
                       pregunta.puntos_pregunta=data['puntosPregunta']
                       pregunta.orden=len(capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])) + 1
                       pregunta.save()
                       hijos = data["hijos"]
                       if hijos:
                          print(hijos)
                          
                          for newOpcion in hijos:
                                
                              Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                              Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                              Opcion.texto_opcion=newOpcion['OpcionText']    
                              Opcion.porc_respuesta=float(newOpcion['value'])  
                                   
                              Opcion.save()
                       print(data)
                    
                       return JsonResponse({"message": "ok"})
                
                #return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                                                                      
@login_required(login_url="/login/")
def getModalQuestion(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request) 
                    print(data)
                    context = {
                     "tipoPreguntas" : ConfTablasConfiguracion.objects.get(valor_elemento=data['data']['tp']).desc_elemento,
                           }
                    print(context)
                    html_template = (loader.get_template('modalAddQuestion.html'))
                    return HttpResponse(html_template.render(context, request))
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)        
@login_required(login_url="/login/")
def getModalNewTof(request):
    
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]
                print(data)
                if data["method"] == "Create": 
                    total=0
                         
                    bloque=capacitacion_EvaluacionesBloques.objects.get(pk=data['fatherId'])   
                    masimapt= bloque.fk_ActividadEvaluaciones.fk_escalasEvaluaciones.maxima_puntuacion
                    testpoint=capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])
                    
                    for item in testpoint:
                        total=total+item.puntos_pregunta
                    print(total)
                    portje=(bloque.peso * masimapt)/100
                    print(portje)
                    if total + Decimal(data['puntosPregunta']) > portje:
                        return JsonResponse({"message":"No"})
                    else: 
                        pregunta=capacitacion_EvaluacionesPreguntas.objects.create()
                    
                        pregunta.fk_evaluacionesBloques_id=data['fatherId']
                        pregunta.fk_tipoPregunta_id=ConfTablasConfiguracion.objects.get(valor_elemento="VoF").pk     
                        pregunta.texto_pregunta=data['textoPregunta']
                        pregunta.puntos_pregunta=data['puntosPregunta']
                        pregunta.orden=len(capacitacion_EvaluacionesPreguntas.objects.filter(fk_evaluacionesBloques_id=data['fatherId'])) + 1
                        pregunta.save()

                        hijos = data["hijos"]
                        if hijos:
                         
                            for newOpcion in hijos:
                                 Opcion=capacitacion_EvaluacionesPreguntasOpciones()
                                 Opcion.fk_capacitacionEvaluacionesPreguntas=pregunta
                                 Opcion.texto_opcion=newOpcion['OpcionText']    
                                 Opcion.porc_respuesta=float(newOpcion['value'])  
                                 Opcion.respuesta_correcta=int(newOpcion['trueFalse'])  
                                     

                                 Opcion.save()

             
                        return JsonResponse({"message": "ok"}) 
            except Exception as e:
                   print(e)
                   return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def sortPreguntas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                context = {}
                data = json.load(request)["data"]

                if data["method"] == "Sort":
                        print(data["order"])
                        for item in data["order"]:
                            pregunta =capacitacion_EvaluacionesPreguntas.objects.get(pk=item["pk"])
                            print(pregunta)
                            pregunta.orden= item["order"]
                            pregunta.save()

                
                return JsonResponse({"message": "Perfect"})     
            except:
                return JsonResponse({"message": "Error"})               


#vistas para el estudiante             
@login_required(login_url="/security/login/")
def indexstudent(request):
    nodoplan=None
                     
    usuario=request.user
    userpu= AppPublico.objects.get(user_id=usuario)
    print(userpu) 
    nodosuser=nodos_gruposIntegrantes.objects.filter(fk_public=userpu)
    if nodosuser.exists():
       nodoplan=nodos_PlanFormacion.objects.filter(fk_gruponodo=nodosuser[0].fk_nodogrupo) 
       if nodoplan.exists():
          print(nodoplan)
          context = {}
          html_template = (loader.get_template('indezstudent.html')) 
       else:
          context = {}   
          html_template = (loader.get_template('page-404._aviso.html'))          
    else:
       context = {}   
       html_template = (loader.get_template('page-404._aviso.html'))   
    return HttpResponse(html_template.render(context, request)) 
@login_required(login_url="/login/")
def renderstemas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
               context = {}
               title=False
               if request.body:                 
                  data = json.load(request)
                                 
                  if data["query"] == "":
                     print(data)
                     nodoplan=None
                     
                     usuario=request.user
                     userpu= AppPublico.objects.get(user_id=usuario)
                     print(userpu) 
                     nodosuser=nodos_gruposIntegrantes.objects.filter(fk_public=userpu)
                     if nodosuser.exists():
                        nodoplan=nodos_PlanFormacion.objects.filter(fk_gruponodo=nodosuser[0].fk_nodogrupo) 
                        print(nodoplan)
                        context = {'usuario':request.user,'plan':nodoplan}
                     else:
                       
                        context = {'usuario':request.user,'plan':nodoplan}
                     html_template = (loader.get_template('rendertemas.html'))
                     return HttpResponse(html_template.render(context, request))    

                
                   
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def renderstudent(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
               context = {}
               title=False
               if request.body:                 
                  data = json.load(request)
                                 
                  if data["query"] == "":
                     print(data)
                     actividad=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion_id=data['id'])
                     context = {"actividad":actividad}
                     html_template = (loader.get_template('renderstudent.html'))
                     return HttpResponse(html_template.render(context, request))    

                
                   
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)       
def verpaginas_student(request):
  id=request.GET.get('id')
  print(id)
  compActividad=capacitacion_ComponentesActividades.objects.get(pk=id)    
  estru=capacitacion_componentesXestructura.objects.get(fk_componetesformacion=compActividad.fk_componenteformacion)    
  print('titi')
  if week(estru,request.user,compActividad):
    if str(compActividad.fk_tipocomponente) =='Leccion':
       print('kola')
       Leccion=capacitacion_Actividad_leccion.objects.get(fk_componenteActividad=compActividad)
       print(Leccion.pk)
       actividad=capacitacion_LeccionPaginas.objects.filter(fk_actividadLeccion_id=Leccion.pk)
       print(actividad.query)
       context = {'actividad': actividad,'id':id,'tema':estru.fk_componetesformacion,'estru':estru.pk,'tipo':str(compActividad.fk_tipocomponente.desc_elemento)}
       print(context)
       html_template = (loader.get_template('actividad.html'))
    elif str(compActividad.fk_tipocomponente) =='Tarea':
         tareas=capacitacion_Actividad_tareas.objects.filter(fk_componenteActividad=compActividad)
         context = {'actividad': tareas,'id':id,'tema':estru.fk_componetesformacion,'estru':estru.pk,'tipo':str(compActividad.fk_tipocomponente.desc_elemento)}
         print(context)
         html_template = (loader.get_template('actividad.html'))
    elif str(compActividad.fk_tipocomponente) =='Evaluacion':
         test=capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad=compActividad)
         test_app=False
         
         usuario=request.user 
         userpu= AppPublico.objects.get(user_id=usuario) 
         nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
         Examen=capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes=nodosuser,fk_ActividadEvaluaciones=test)   
         print(Examen)
         print('lo')
         if Examen.exists():
             for item in Examen:
                
                 if item.puntuacion_obtenida>=test.calificacion_aprobar:
                    test_app=True 
                        
         context = {'test':test,'id':id,'test_app':test_app,'Examen':Examen,'tema':estru.fk_componetesformacion,'estru':estru.pk}
         print(context)
         html_template = (loader.get_template('indestest.html')) 
    elif str(compActividad.fk_tipocomponente) =='Sesiones':
         sesiones=capacitacion_Actividad_Sesiones.objects.get(fk_componenteActividad=compActividad)
         programar=capacitacion_ActSesiones_programar.objects.get(id_capacitacionActividadSesiones=sesiones)
         context = {'programar': programar,'sesiones':sesiones,'id':id,'tema':estru.fk_componetesformacion,'estru':estru.pk,'tipo':str(compActividad.fk_tipocomponente.desc_elemento)}
         print(context)
         html_template = (loader.get_template('student_sesiones.html'))         
  else:
      context={}
      html_template = (loader.get_template('page-aviso.html')) 
  return HttpResponse(html_template.render(context, request))
            
def logUser(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            usuario=request.user
            userpu= AppPublico.objects.get(user_id=usuario)
            print(userpu) 
            nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
            rol=usuario.fk_rol_usuario
            print(rol)
            try:
                if request.body:
                    data=json.load(request)
                    print(data) 
                    idA= data["pk"]
                    idStr=data['estru']
                    fecha = datetime.datetime.now()
                    print(fecha)
                    culminado = data["estado"]
                    historial=capacitacion_HistoricoActividades.objects.filter(fk_componenteXestructura_id=data['estru'])
                    if historial.exists():
                     datos=json.loads(historial[0].datos_resumen)
                     print(datos)
                     tema=datos['datos_resumen'][0]['tema']
                     if int(tema) ==capacitacion_ComponentesActividades.objects.get(pk=idStr).fk_componenteformacion_id: 
                         print('no')
                    else:
                      if culminado == 0:
                       topico = capacitacion_ComponentesActividades.objects.get(pk=idStr).fk_componenteformacion
                       lecciones =capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=topico) 
                       print('hola') 
                       hayPrimero = False
                       for leccion in lecciones:
                           primer=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=nodosuser, fk_componenteActividades=leccion)
                           if primer.exists():
                              hayPrimero = True
                              break
                       if hayPrimero == False:  
                          print('mensaje')
                      update = capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=nodosuser, fk_componenteActividades=idA)
                      if update.exists():
                        historia = update.order_by("-fecha_realizado")[0]
                        if historia.culminado == 1 or historia.culminado == culminado:
                           return JsonResponse({"message":"ok"}, status=200)
                      else:
                         historia = capacitacion_ActividadesTiempoReal()
                         historia.fecha_realizado = fecha
                      historia.culminado = culminado
                      historia.fk_componenteActividades_id = idA
                      historia.fk_nodo_Grupo_integrantes=nodosuser
                      historia.fk_componenteXestructura_id=idStr
                      historia.save()
                        
                      finalizar_componente(userpu,idStr)  
                return JsonResponse({"message":"ok"}, status=200)                
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)     
   
def imagesave(request):
    if request.method == "POST":

        myfile = request.FILES['imagen']
        print(myfile)
        Ruta = settings.UPLOAD_ROOT + '/plantillasimg'    
        fs = FileSystemStorage(location=settings.UPLOAD_ROOT)       
        nombreImagen = str(request.user) + ".png"        
        try:

            os.mkdir(os.path.join(Ruta))

        except:
    
            pass

        fs.delete(Ruta + '/' + str(myfile))
        fs.save(Ruta + '/' + str(myfile), myfile)
        return JsonResponse({'mensaje': 'Changes applied successfully', 'ruta': (nombreImagen)})
def borrarImagenes(request):
    if request.method == "POST":
        
        id=request.POST.get('ids')
        componente=componentesFormacion.objects.get(pk=id)
        if componente.path_plantilla_certificado and componente.path_plantilla_certificado != '':
    
            fs = FileSystemStorage(location=settings.UPLOAD_ROOT)
            nombreImagen = componente.path_plantilla_certificado
            print(nombreImagen)
            Ruta = settings.UPLOAD_ROOT + '/plantillasimg'

            fs.delete(Ruta + '/' + nombreImagen)

            
            componente.path_plantilla_certificado=''
            componente.save()

            return JsonResponse({'mensaje': 'Image deleted'})

        else:

            return JsonResponse({'mensaje': 'There is no image to remove'})
def takeExam(request):        
    id=request.GET.get('id')
    print(id)
    method=request.GET.get('method',None)
    usuario=request.user 
    userpu= AppPublico.objects.get(user_id=usuario) 
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
    test=capacitacion_ActividadEvaluaciones.objects.get(fk_componenteActividad_id=id)    
    print(test.pk)
    estru=capacitacion_componentesXestructura.objects.get(fk_componetesformacion=test.fk_componenteActividad.fk_componenteformacion)
    bloques=capacitacion_EvaluacionesBloques.objects.filter(fk_ActividadEvaluaciones=test)
    tipo=''
    print(method)
    if method:
       tipo='retake'
       print(tipo)
       Examen=capacitacion_Examenes.objects.get(fk_ActividadEvaluaciones=test
                                                )
       Examen.status_examen=0       
       Examen.puntuacion_obtenida=0
       Examen.fecha_inicio=datetime.datetime.now() 
       Examen.fecha_final=None    
       resultados=capacitacion_ExamenesResultado.objects.filter(fk_capacitacionExamenes=Examen)       
       resultados.delete()       
       Examen.save()
       historia = capacitacion_ActividadesTiempoReal.objects.get(fk_nodo_Grupo_integrantes=nodosuser,fk_componenteActividades = test.fk_componenteActividad,fk_componenteXestructura = estru)
       historia.fecha_realizado = datetime.datetime.now()
       historia.culminado = 0
       historia.fk_componenteActividades = test.fk_componenteActividad
       historia.fk_componenteXestructura = estru
       historia.fk_nodo_Grupo_integrantes= nodosuser
       historia.save()
    else:
        tipo='Save'  
        print(tipo)  
        print(method)          
        teststart=capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes=nodosuser,fk_ActividadEvaluaciones=test)
        if not teststart.exists():
           Examen=capacitacion_Examenes.objects.create()
           Examen.fecha_inicio=datetime.datetime.now()
           Examen.fk_nodo_Grupo_integrantes=nodosuser
           Examen.fk_ActividadEvaluaciones=test
           Examen.nro_repeticiones=0
           Examen.status_examen=0 
           Examen.puntuacion_obtenida=0
           time=None
           if test.duracion != None:
                   
              time=Examen.fecha_inicio+ datetime.timedelta(0,(test.duracion*60))
              time=time.strftime("%b %d %Y %H:%M:%S")
                 


           Examen.save()
           historia = capacitacion_ActividadesTiempoReal()
           historia.fecha_realizado = datetime.datetime.now()
           historia.culminado = 0
           historia.fk_componenteActividades = test.fk_componenteActividad
           historia.fk_componenteXestructura = estru
           historia.fk_nodo_Grupo_integrantes= nodosuser
           historia.save()
       
        else:
           Examen=capacitacion_Examenes.objects.get(fk_nodo_Grupo_integrantes=nodosuser,fk_ActividadEvaluaciones=test)   
       
    context = {'bloques':bloques,'test':test,'examen_id': Examen.pk,'tipos':tipo}
    print(context)
    html_template = (loader.get_template('contenidoExamen.html'))
    return HttpResponse(html_template.render(context, request))    
def contenidoTest(request):
   
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            data = json.load(request)["data"]            
            print(data)
            usuario=AppPublico.objects.get(user_id=request.user)
            if data["method"] == "Save":
                respuestas=data["respuestas"] 
                if respuestas:
                    total=0 
                    examen=capacitacion_Examenes.objects.get(pk=data['examenesid'])          
                    for resp in respuestas:
                        opcionRespuesta=capacitacion_ExamenesResultado.objects.create()
                        opcion=capacitacion_EvaluacionesPreguntasOpciones.objects.get(pk=resp['opcionID'])
                     
                        opcionRespuesta.fk_capacitacionEvaluacionesPreguntasOpciones=opcion
                        opcionRespuesta.fk_capacitacionExamenes=examen
                        pregunta=capacitacion_EvaluacionesPreguntas.objects.get(pk=resp['idPregunta'])
                        
                        if(resp['tipoPregunta']=='Simple'):
                            
                            if(opcion.respuesta_correcta):
                                 
                               opcionRespuesta.puntos_obtenidos=pregunta.puntos_pregunta                         
                               examen.puntuacion_obtenida=examen.puntuacion_obtenida+pregunta.puntos_pregunta
                        if(resp['tipoPregunta']=='VoF'):
                          if capacitacion_EvaluacionesPreguntasOpciones.objects.filter(pk=resp['opcionID'],respuesta_correcta=resp['isCorrect']).exists():   
                             opcionRespuesta.respuesta_correcta=resp['isCorrect'] 
                             opcionRespuesta.puntos_obtenidos=opcion.porc_respuesta
                        if(resp['tipoPregunta']=='Multiple'):
                           
                            if(str(opcion.pk) == resp['opcionID']):
                                
                                opcionRespuesta.puntos_obtenidos=opcion.porc_respuesta   
                        opcionRespuesta.save() 
                        if(resp['tipoPregunta']=='VoF'): 
                           
                            print(opcionRespuesta.respuesta_correcta)
                            print(opcion.respuesta_correcta)
                            if opcion.respuesta_correcta==opcionRespuesta.respuesta_correcta :
                               print('si') 
                               examen.puntuacion_obtenida=examen.puntuacion_obtenida+opcion.porc_respuesta
                            
                            
                        if(resp['tipoPregunta']=='Multiple'):
                             
                             examen.puntuacion_obtenida=examen.puntuacion_obtenida+opcion.porc_respuesta
                    print(examen.puntuacion_obtenida)                 
                    opcionRespuesta.save()
                    if examen.puntuacion_obtenida>=examen.fk_ActividadEvaluaciones.calificacion_aprobar:
                        
                        examen.status_examen=1
                    else:
                        
                        examen.status_examen=2
                    examen.fecha_final=datetime.datetime.now()
                    examen.save()
                    if data['tipo'] == 'retake':
                       examen.nro_repeticiones= examen.nro_repeticiones+1
                    if examen.puntuacion_obtenida>=examen.fk_ActividadEvaluaciones.calificacion_aprobar:
                        estado=True
                        examen.status_examen=1
                    else:
                        estado=False
                        examen.status_examen=2
                    examen.save()    
                    log=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes, fk_componenteActividades=examen.fk_ActividadEvaluaciones.fk_componenteActividad)
                    esUpdate =True
                    if log.exists():
                        if esUpdate ==True:
                            new=capacitacion_ActividadesTiempoReal.objects.get(pk=log[0].pk)
                            if new.culminado == 0:
                            # new.fecha = timezone.now()
                                new.culminado = estado
                                new.save()
                        else:
                                log.delete()
                                historia = capacitacion_ActividadesTiempoReal()
                                historia.fecha_realizado = datetime.datetime.now()
                                historia.culminado = estado
                                historia.fk_componenteActividades = examen.fk_ActividadEvaluaciones.fk_componenteActividad
                                historia.fk_nodo_Grupo_integrantes = examen.fk_nodo_Grupo_integrantes
                                historia.fk_componenteXestructura = capacitacion_componentesXestructura.objects.get(fk_componetesformacion=examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion)
                                historia.save()  
                    if examen.puntuacion_obtenida>=examen.fk_ActividadEvaluaciones.calificacion_aprobar:
                       if verifylast(examen) == examen.fk_ActividadEvaluaciones.fk_componenteActividad:                                    
                          if finalizar_componente(usuario,capacitacion_componentesXestructura.objects.get(fk_componetesformacion=examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion).pk):
                              fecha_ini=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes,culminado=1,fk_componenteActividades__fk_componenteformacion=examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion).order_by('fk_componenteActividades')[0].fecha_realizado
                              fecha_fin=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes,culminado=1,fk_componenteActividades__fk_componenteformacion=examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion).order_by('-fk_componenteActividades')[0].fecha_realizado
                              programar=[]
                              obj={}
                              datos = {}
                              obj["fecha_ini"]=str(fecha_ini) 
                              obj["fecha_fin"]=str(fecha_fin)              
                              obj["tema"]=str(examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion)
                              obj["ultima_Actividad"]=str(examen.fk_ActividadEvaluaciones.fk_componenteActividad)
                              obj["nota"]=str(examen.puntuacion_obtenida)
                              programar.append(obj or 0)
                              datos['datos_resumen']=programar
                              print(datos)
                              historial=capacitacion_HistoricoActividades.objects.create()
                              historial.fk_componenteXestructura=capacitacion_componentesXestructura.objects.get(fk_componetesformacion=examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion)
                              historial.fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes
                              historial.datos_resumen=json.dumps(datos)
                              historial.estatus_lider=0
                              historial.save()
                              deletehistori=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes, fk_componenteActividades__fk_componenteformacion = examen.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion)
                              deletehistori.delete()
                            #   deleteop=capacitacion_ExamenesResultado.objects.filter(fk_capacitacionExamenes=examen)
                            #   deleteop.delete()
                            #   deletetest=capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes=examen.fk_nodo_Grupo_integrantes,fk_ActividadEvaluaciones=examen)
                            #   deletetest.delete()          
            return JsonResponse({"message": "Perfect"})         
def viewresult_test(request):
    id=request.GET.get('id')
    print(id)
    usuario=request.user
    userpu= AppPublico.objects.get(user_id=usuario) 
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
    test=capacitacion_Examenes.objects.get(pk=id,fk_nodo_Grupo_integrantes=nodosuser)
    context = {'test':test,'id':test.fk_ActividadEvaluaciones.fk_componenteActividad_id}
   
    html_template = (loader.get_template('ver_resultados_test.html'))
    return HttpResponse(html_template.render(context, request))        
def getModalNewnotifi(request):            
   if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    
                    if data["method"] == "Show":
                       print(data)
                       tipo=''
                       notifi=capacitacion_NotificacionesMensajesXactividad.objects.filter(fk_actividad_componente=data['id'])
                       print(notifi)
                       if notifi.exists():
                           tipo=capacitacion_NotificacionesMensajesXactividad.objects.get(fk_actividad_componente=data['id'])
                           context = {'tipo':tipo}
                       else:
                           
                           context = {}   
                       print(context)
                       html_template = (loader.get_template('modalAddnotifi.html'))
                       return HttpResponse(html_template.render(context, request))            
                    elif data["method"] == "Create":
                        print(data)
                        notifis=capacitacion_NotificacionesMensajesXactividad.objects.filter(fk_actividad_componente=data['id'])
                        if notifis.exists():
                           notifiedit=capacitacion_NotificacionesMensajesXactividad.objects.get(fk_actividad_componente=data['id'])
                           notifiedit.cuando=data['data']['modalidad_Cuando']
                           notifiedit.tipo=data['data']['modalidad'] 
                           if data['data']['modalidad'] == 0:
                              mensaje=Comunication_MsjPredeterminado.objects.filter(tipo_msj='mensaje') 
                              if mensaje.exists():                               
                                 notifiedit.fk_notificacionActividad=mensaje[0].pk
                           notifiedit.save()
                        else:    
                         notifi=capacitacion_NotificacionesMensajesXactividad.objects.create()
                         notifi.cuando=data['data']['modalidad_Cuando']
                         notifi.tipo=data['data']['modalidad']
                         notifi.fk_actividad_componente=data['id']
                         notifi.fk_tipoActividad=capacitacion_ComponentesActividades.objects.get(pk=data['id']).fk_tipocomponente
                         #print(capacitacion_ComponentesActividades.objects.get(pk=data['id']).fk_tipocomponente)
                         if data['data']['modalidad'] == 0:
                            mensaje=Comunication_MsjPredeterminado.objects.filter(tipo_msj='mensaje') 
                            if mensaje.exists():                               
                               notifi.fk_notificacionActividad=mensaje[0].pk
                             
                         notifi.save()
                        return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getModalinstru(request):            
   if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)                    
                    if data["method"] == "Show": 
                       print(data) 
                       bloques=capacitacion_EvaluacionesBloques.objects.get(pk=data['id']) 
                       context = {'bloques':bloques}  
                       
                       html_template = (loader.get_template('Modalinstru.html'))
                       return HttpResponse(html_template.render(context, request))                      
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
@login_required(login_url="/security/login/")
def indexHistory(request):
    
    user = request.user
    rol=user.fk_rol_usuario
    persona=AppPublico.objects.get(user_id=user)  
    context = {}
   
    if str(rol) == "Lider" :
       grupos=nodos_grupos.objects.filter(fk_liderGrupo=persona)                          
       if grupos.exists():
          integrantes=nodos_gruposIntegrantes.objects.filter(fk_nodogrupo__fk_liderGrupo=persona)  
          context = {'keys' : TITULOPUBLIC,'plan': paginas(request, integrantes),'grupos':grupos,'integrantes':integrantes}
                        
          html_template = (loader.get_template('Historial.html'))
    elif  str(rol) == "Estudiante" : 
          integrantes=nodos_gruposIntegrantes.objects.filter(fk_public=persona)  
          context = {'keys' : TITULOPUBLIC,'plan': paginas(request, integrantes),'rol':str(rol)}
                       
          html_template = (loader.get_template('Historial.html'))
    else:
        html_template = (loader.get_template('page-403.html'))
    return HttpResponse(html_template.render(context, request))

                  
def Renderdetalle(request):            
   if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)                    
                    if data["query"] == "": 
                       print(data)                                             
                       persona=AppPublico.objects.get(pk=data['id'])
                       print(persona)
                       integrante=nodos_gruposIntegrantes.objects.get(fk_public=persona)
                       integrante_historia=capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=integrante)
                       integrante_resumen=capacitacion_HistoricoActividades.objects.filter(fk_nodo_Grupo_integrantes=integrante)
                       img = persona.user_id.url_imagen
                       mail=persona.user_id.email
                       context = {'img': img if img and img != "" else None,'historia':integrante_historia,'historia_resumen':integrante_resumen,'email':mail}                      
                       html_template = (loader.get_template('detalle_integrante.html'))
                       return HttpResponse(html_template.render(context, request))                      
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                                               
def paginas(request, obj, range = 5):
    
    page = request.GET.get('page', 1) if request.GET else request.POST.get('page', 1)
    # print(request.GET.get('page') if request.GET.get('page') else "nada get")
    # print(request.POST.get('page') if request.POST.get('page') else "nada post")

    paginator = Paginator(obj, sys.maxsize if range and range == 'TODOS' else range if range else 5)
    # paginator = Paginator(obj, sys.maxsize if range and range == 'ALL' else range if range else 5)

    try:

        pages = paginator.page(page)
        # print(page)

    except PageNotAnInteger:
        # print("error 1")
        pages = paginator.page(1)

    except EmptyPage:
        # print("error 2")
        pages = paginator.page(paginator.num_pages)

    return pages           
def paginarhistory(request):
    
    
    
    filtro = request.POST.get('filtro', None)    
    nodo = request.POST.get('nodo', None)
       
    plan = nodos_gruposIntegrantes.objects.all()
        

   

    if filtro:

        filtro = filtro.strip()
        plan = plan.filter(Q(fk_public__nombre__icontains=filtro) | Q(fk_public__user_id__username__icontains=filtro) )
    if nodo:        
        plan = plan.filter(fk_nodogrupo_id=nodo)
    
    
    

    pagina = render_to_string('paginashistory.html', {'plan': paginas(request, plan, 5)})
    tabla = render_to_string('contenidotablahistory.html', {'keys' : TITULOPUBLIC,'plan': paginas(request, plan, 5) })

    

    response = {
        'paginas': pagina,
        'contenido' : tabla
    }

    return JsonResponse(response)
def getModalPublicar(request):            
   if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)
                    if data["method"] == "Show":
                       print(data)
                       siexiste=""
                       publicacion=capacitacion_tiempoxevaluaciones.objects.filter(fk_evaluacion_id=data['id'])
                       if publicacion.exists():
                          siexiste=publicacion[0]
                       else:
                          siexiste=""
                       context={'publica':siexiste}        
                       html_template = (loader.get_template('ModalPublicartest.html'))
                       return HttpResponse(html_template.render(context, request))            
                    
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def savetestpublicar(request):
     if request.method == "POST":
          if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {}
            modelo = {}
            try:
                if request.body:
                    data = json.load(request)['data']
                    print(data)
                    if data['method']== 'Create':
                       test=capacitacion_ActividadEvaluaciones.objects.get(pk=data['pk'])
                       hijos = data["hijos"]
                       if hijos:
                          print(hijos)
                               
                          for newOpcion in hijos:
                                
                              Opcion=capacitacion_tiempoxevaluaciones()
                              Opcion.Desde=newOpcion['Opciondesde'] 
                              Opcion.Hasta=newOpcion['Opcionhasta']       
                              Opcion.fk_evaluacion=test
                              Opcion.fk_nodos_id=newOpcion['id'] 
                              Opcion.save() 
                       print(data)
                       return JsonResponse({"message":"ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)          
def RenderListaspublicar(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                user = request.user
                rol=user.fk_rol_usuario 
                print(rol) 
                context={}
                title=False
                data = json.load(request)
                grupos=""
                if data["method"] == "Show":
                    if str(rol) == 'Lider':
                       print('hola') 
                       publico=AppPublico.objects.get(user_id=user) 
                       print(user)
                       grupos=nodos_grupos.objects.filter(fk_liderGrupo=publico,status_grupo=60) 
                       print(grupos)
                       context = {'grupo':grupos}
                       html_template = (loader.get_template('combolidernodo.html'))
                       return HttpResponse(html_template.render(context, request)) 
                    else:
                      print(data)
                      grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,status_grupo=60)
                      print(grupos)
                      context = {'grupo':grupos}
                      html_template = (loader.get_template('comboboxnodo.html'))
                      return HttpResponse(html_template.render(context, request)) 
                elif data['method'] == "Hijos":
                    print(data)
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=data['pk'])
                    print(grupos)
                    if grupos.exists():
                        
                       context = {'grupo':grupos}
                    else:
                       hijo=nodos_grupos.objects.filter(if_gruponodo=data['pk'])
                       context = {'grupo':hijo,'elegido':hijo[0]}
                    html_template = (loader.get_template('comboboxnodo.html'))
                    return HttpResponse(html_template.render(context, request))
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def Edittestpublicar(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                context = {}
                data = json.load(request)["data"]   
                
                if "delete" in data:
                    print(data)
                   
                    actividad=capacitacion_tiempoxevaluaciones.objects.get(pk=data['id'])
                    print(actividad)
                    actividad.delete()
                    return JsonResponse({"message": "Deleted"})
                if "idFind" in data:
                    print(data)
                    
                    childs = capacitacion_tiempoxevaluaciones.objects.filter(fk_evaluacion_id=data["idFind"])
                    listaChilds = list(childs.values())
                    print(listaChilds)
                    return JsonResponse({ "childs":listaChilds}, safe=False)
                
                if data["method"] == "Update":
                    print(data)
                    test=capacitacion_ActividadEvaluaciones.objects.get(pk=data['pk'])
                    childs=capacitacion_tiempoxevaluaciones.objects.filter(fk_evaluacion_id=test.pk)
                    hijos = data["hijos"]
                    if hijos:
                            
                       childs.delete()
                                
                       for newOpcion in hijos:
                                
                           Opcion=capacitacion_tiempoxevaluaciones()
                           Opcion.Desde=newOpcion['Opciondesde'] 
                           Opcion.Hasta=newOpcion['Opcionhasta']       
                           Opcion.fk_evaluacion_id=test.pk
                           Opcion.fk_nodos_id=newOpcion['id'] 
                           Opcion.save() 
                    
                
                    return JsonResponse({"message": "ok"})
            except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)           