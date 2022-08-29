from unicodedata import category, decimal
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from ..App.models import ConfTablasConfiguracion
from ..Capacitacion.models import Estructuraprograma
import time, json
from decimal import Decimal
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def index(request):
    
    # user = request.user.extensionusuario
    # rol = user.CtaUsuario.fk_rol_usuario.desc_elemento
    # publico = user.Publico
    context = {}
    # context['segment'] = 'academic'
    # context['rol'] = rol
    # context['user'] = publico
    # if rol == "Admin" or rol == "Student" or rol == "Teacher":
    html_template = (loader.get_template('gestor_index.html'))
    # else:
    #     return HttpResponseForbidden()
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
                   categorias=ConfTablasConfiguracion.obtenerHijos("Categoria") 
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
                   print(data)
                   if procesos.exists():
                      paginator = Paginator(procesos, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"]
                      context = {"page": page,"limit": limit,'procesos':procesos,'padre':data['id'],'data':lista}
                      #print(context)
                      html_template = (loader.get_template('renderizadopro.html'))
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {'title':title,'padre':data['id']}
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
def indextwo(request):
    id=request.GET.get('id')
   
    context = {'id':id}
    print(context)
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
                   units=Estructuraprograma.objects.filter(fk_estructura_padre_id=data['pk'],valor_elemento="Module")
                   if units.exists(): 
                      paginator = Paginator(units, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"]
                      context = {"page": page,"limit": limit,'units':units,'pk':data['pk'],'padre':data['pk'],'data':lista}             
                      html_template = loader.get_template( 'contenidounidades.html' )
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {'title':title}             
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
                   cursos=Estructuraprograma.objects.filter(fk_estructura_padre_id=data['id'],valor_elemento="Courses")
                   if cursos.exists():
                      paginator = Paginator(cursos, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"] 
                      context = {"page": page,"limit": limit,'cursos':cursos,'pk':data['id'],'padre':data['id'],'data':lista}             
                      html_template = loader.get_template( 'renderizarcursos.html' )
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {'title':title,'pk':data['id']}             
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
                    modelo = Estructuraprograma.objects.get(pk=data["id"])    
                    categorias = ConfTablasConfiguracion.obtenerHijos(valor="Categoria")
                    context = {"categorias": categorias, "modelo": modelo}
                    html_template = (loader.get_template('modaladdcursos.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data["method"] == "Delete":
                    cursos = Estructuraprograma.objects.get(pk=data["id"])
                    cursos.delete()
                    return JsonResponse({"message":"Deleted"}) 
                elif data["method"] == "Update":
                     cursos = Estructuraprograma.objects.get(pk=data["id"])
                elif data['method'] == "Create":
                   proAdd=Estructuraprograma.objects.get(pk=data['id']).fk_categoria_id
                   print(proAdd)
                   cursos=Estructuraprograma()
                   cursos.fk_estructura_padre_id=data['id']
                   cursos.fk_categoria_id=proAdd
                cursos.valor_elemento="Courses"
                cursos.descripcion=data['data']['resumenProgram']    
                cursos.url=data['data']['urlProgram']         
                cursos.Titulo=data['data']['descriptionProgram']
                cursos.peso_creditos=Decimal(data['data']['creditos'].replace(',','.'))
                cursos.save()
                return JsonResponse({"message":"ok"})
                
            context = {}             
            html_template = loader.get_template( 'modaladdcursos.html' )
            return HttpResponse(html_template.render(context, request)) 
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)