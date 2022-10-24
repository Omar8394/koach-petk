import json, math
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.template import loader
import sys
from ..App.models import ConfMisfavoritos,ConfSettings,ConfSettings_Atributo,ConfTablasConfiguracion
from ..Capacitacion.models import EscalasEvaluaciones,EscalasCalificacion
from django.shortcuts import render
from django.template.defaulttags import register
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
@register.filter
def hasprefer(id):
   lista=[] 
   
   haspre= ConfSettings.objects.filter(fk_modulo_setting=id)
   for item in haspre:
       id=item.idconfig_setting
       #title=item.titulo_setting
       lista.append(id)
       
   print(haspre)
   return lista
@register.filter
def hasprefername(id):
   
   
   haspre= ConfSettings.objects.filter(fk_modulo_setting_id=id)
   
   print(haspre)
   return haspre 
@register.filter
def hasprefernameatri(id):
   
   
   haspre= ConfSettings_Atributo.objects.filter(fk_setting_padre_id=id)
   
   print(haspre)
   return haspre
@register.filter(name='jsonrango')
def jsonrango(datos):
  if datos==None or datos=="" or datos=={}:
      return ""
  tlf=None
  data = json.loads(datos)
  print(data)
  
  
  if data==None or data=="" or data=={}:
      return ""

  if   'min' in data :
     return data['min']
  else:
      return ""
@register.filter(name='jsonrangotwo')
def jsonrango(datos):
  if datos==None or datos=="" or datos=={}:
      return ""
  tlf=None
  data = json.loads(datos)
  print(data)
  
  
  if data==None or data=="" or data=={}:
      return ""

  if   'max' in data :
     return data['max']
  else:
      return ""
def mostrarfavoritos(request): 
    context = {}

    if request.method == "POST":
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:
                
                data = json.load(request)

                if data['acceso'] == 'show':

                    tab_data = ConfMisfavoritos.objects.all()
                    
                    context = {'data':tab_data}
                
                    html_template = loader.get_template( 'App/Favorito/mostrarFavoritos.html' )
                    return HttpResponse(html_template.render(context, request))
                
                if data['acceso'] == 'vaciar':

                    for item in data['idCheckbox']:
                        
                        favoritos = ConfMisfavoritos.objects.filter(pk=data['idCheckbox'][item])
                        favoritos.delete()
                
                    return JsonResponse({"message":"vacio"})

                if data['acceso'] == 'delete':

                    for item in data['idCheckdelete']:
                        
                        favoritos = ConfMisfavoritos.objects.filter(pk=data['idCheckdelete'][item])
                        favoritos.delete()
                
                    return JsonResponse({"message":"delete"})

                if data['acceso'] == 'edit':

                    favoritos = ConfMisfavoritos.objects.get(pk=int(data['item']))
                    favoritos.descripcion_url = data['item1']
                    favoritos.save()
                
                    return JsonResponse({"message":"edit"})
    
    
 
def añadirFavoritos(request):    
    context = {}

    if request.method == "POST":
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:
                data= json.load(request)

                if data['acceso'] == 'validar':
                    tab_data = ConfMisfavoritos.objects.filter(direccion_url=data['item']).count()
                    
                    return JsonResponse({"num":tab_data})

                if data['acceso'] == 'save':
                    tab_data = ConfMisfavoritos.objects.filter(direccion_url=data['item']).count()

                    if tab_data == 0:

                        favoritos = ConfMisfavoritos()

                        favoritos.idpublic=2
                        favoritos.direccion_url=data["item"]
                        favoritos.descripcion_url=data["item1"]

                        favoritos.save()

                        return JsonResponse({"message":"Perfect"})
                    else:
                        return JsonResponse({"message":"existe"})



                
                

def configuracion(request):
    
    return render(request, "configuraciones_generales.html")
def preferencias(request):
    modules=ConfTablasConfiguracion.obtenerHijos("Modulos")
    atri=ConfSettings.objects.all()
    print(atri)
    context = {'modules':modules,'atri':atri}            
    html_template = loader.get_template( 'preferemcias.html' )
    return HttpResponse(html_template.render(context, request))
def saveprefer(request):
  try:     
    title=request.POST.get('prefertitle')
    
    desr=request.POST.get('preferdesr')
    modulo=request.POST.get('prefermodulo')
    setting=ConfSettings()
    setting.titulo_setting=title
    setting.descripcion_setting=desr
    setting.fk_modulo_setting_id=modulo
    setting.save()
    print(title)
    print(desr)
    print(modulo)
    return JsonResponse({"message": "Perfect"})
  except Exception as e:
         print(e)
         return JsonResponse({"message":"error"}, status=500)
                
def getmodalprefer(request):
    
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         try:   
            if request.body:
                context={}
                data = json.load(request) 
                if data['method'] == 'show':
                   modules=ConfTablasConfiguracion.obtenerHijos("Modulos")
                   dato=ConfTablasConfiguracion.obtenerHijos("Tipo_dato")
                   set=ConfTablasConfiguracion.obtenerHijos("Atributo")
                   context = {'modules':modules,'dato':dato,'set':set} 
                   html_template = (loader.get_template('modalpreferen.html'))
                   return HttpResponse(html_template.render(context, request))
                elif data['method'] == 'Create':
                    rango={}
                    
                    for key in data["data"]:
                        if key=="checkDurationCB":
                           vale=1
                           print(vale)
                        else:
                           vale=0
                           print(vale)
                          
                        if key == "checkDuration":
                           print('ket')
                           rango["min"]=data["data"]["min_points"]
                           rango["max"]=data["data"]["max_points"]
                           range=json.dumps(rango)
                           print(str(range))
                        else:
                            range=rango
                    guardaset=ConfSettings_Atributo()
                    guardaset.Atributo=data['data']['set']
                    guardaset.fecha_activo=data['data']['entregaHomework']
                    guardaset.status_setting=1
                    guardaset.rangovalor_setting=json.dumps(rango)
                    guardaset.valor_setting=data['data']['titleCourse']
                    guardaset.permite_borrar=vale
                    guardaset.fk_setting_padre_id=data['data']['categoriasProcess']
                    guardaset.fk_tipo_dato_setting_id=data['data']['dato']
                    guardaset.save()
                    print(data)
                return JsonResponse({"message": "Perfect"}) 
         except Exception as e:
                print(e)
                return JsonResponse({"message":"error"}, status=500)
   

def combobox(request):

    valor=request.GET.get('valor')
    print(valor)
    data={'opcion1': metodo_llenar_combo(valor)}

    html_template = (loader.get_template('combobox.html'))
    
    
    return HttpResponse(html_template.render(data, request))




def metodo_llenar_combo(valor):
    valor1=valor
    result1=ConfSettings.objects.filter(fk_modulo_setting=valor1)
    list=[]

    for file in result1:
        
        list.append(file)
        
    return list 
def setprefer(request) :
    ttv=request.POST
    rango={}
    print(ttv)
    pos=request.POST.get('tipo')   
    estructura=request.POST.get('value') 
    id=request.POST.get('campo_bd')
    rmi=request.POST.get('rmi') 
    rma=request.POST.get('rma')
    setting=ConfSettings_Atributo.objects.get(pk=id)
    if pos == 'status':
       setting.status_setting=estructura
    elif pos == 'borrar':
        setting.permite_borrar=estructura
    elif pos == 'repeatstwo':
        setting.valor_setting=estructura
    elif pos == 'edit':
        rango["min"]=rmi
        rango["max"]=rma                       
        setting.rangovalor_setting=json.dumps(rango)
    setting.save()
    print(estructura)
    print(id)
    return JsonResponse({"message":"Perfect"})
def tablesettings(request) :
    
    context = {}            
    html_template = loader.get_template( 'systemata.html' )
    return HttpResponse(html_template.render(context, request))
def getcontentablas(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if request.body:
                context={}
                data = json.load(request)
                print(data)
                father=ConfTablasConfiguracion.obtenerHijos("padre")
                if data["query"] == "":
                   
                     
                   context = {'father':father}  
                   print(context)          
                   html_template = loader.get_template( 'tables.html' )
                   return HttpResponse(html_template.render(context, request)) 
                elif  data["query"] != "":  
                      print(data)
                      father = father.filter(desc_elemento__icontains=data["query"])
                      context = {'father':father}            
                      html_template = loader.get_template( 'tables.html' )
                      return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
   

def gethijos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          try: 
            if request.body:
                context={}
                data = json.load(request)
                print(data)
                lista = []
                if data["query"] == "":
                   hijos=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=data["ids"])
                   
                   paginator = Paginator(hijos, data["limit"])
                   lista = paginator.get_page(data["page"])
                   page = data["page"]
                   limit = data["limit"]
                   context = {"page": page,"limit": limit,'padre':data["ids"],'data':lista}            
                   html_template = loader.get_template( 'verhijos.html' )
                   return HttpResponse(html_template.render(context, request))
          except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
       
                
def deletehijos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if request.body:
                context={}
                data = json.load(request)
                print(data)
                if data["query"] == "delete":
                   delethijos=ConfTablasConfiguracion.objects.get(pk=data["id"])
                   delethijos.delete()
                   return JsonResponse({"message":"delete"})
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
              
def edithijos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          try:
            if request.body:
                context={}
                data = json.load(request)
                print(data)
                if data["edit"] == "find":
                   editson=ConfTablasConfiguracion.objects.filter(id_tabla=data["id"])
                   context = {'hijos':editson}            
                   html_template = loader.get_template( 'modalAddSetting.html' )
                   return HttpResponse(html_template.render(context, request))
                elif data["edit"] == "edit":
                     editar=ConfTablasConfiguracion.objects.get(pk=data['data']['father'])
                     editar.desc_elemento=data['data']["descripcion"] 
                     editar.tipo_elemento=1
                     editar.permite_cambios=data['data']["permiteCambios"] 
                     editar.valor_elemento=data['data']["valorElemento"] 
                     editar.mostrar_en_combos=data['data']["mostrarEnCombos"] 
                     editar.maneja_lista=data['data']["manejaLista"]
                     editar.datos_adicional= data['data']["valoradd"]
                     editar.tipo_dato=1
                    
                     editar.save()
                     print(data) 
                     return JsonResponse({"message":"ok"})
          except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
              
               
def getModalSetting(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
          try: 
            if request.body:
                context={}
                data = json.load(request)
               
                print(data)
                if data["query"] == "":
                   #print(data)
                   context = {"tables": ConfTablasConfiguracion.objects.all(),"add":True}
                   html_template = (loader.get_template('modalAddSetting.html'))
                   return HttpResponse(html_template.render(context, request))
                elif data["query"] == "save":
                    newConfig = ConfTablasConfiguracion()
                    newConfig.desc_elemento=data['data']["descripcion"] 
                    newConfig.tipo_elemento=1
                    newConfig.permite_cambios=data['data']["permiteCambios"] 
                    newConfig.valor_elemento=data['data']["valorElemento"] 
                    newConfig.mostrar_en_combos=data['data']["mostrarEnCombos"] 
                    newConfig.maneja_lista=data['data']["manejaLista"]
                    newConfig.datos_adicional= data['data']["valoradd"]
                    newConfig.tipo_dato=1
                    newConfig.fk_tabla_padre_id=data['data']["father"]
                    newConfig.save()
                    #print(data)
                    return JsonResponse({"message":"Perfect"})
                
          except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
@login_required(login_url="/login/")
def scales(request):
    # user = request.user.extensionusuario
    # rol = user.CtaUsuario.fk_rol_usuario.desc_elemento

    # if rol != 'Admin':
    #     return HttpResponseForbidden()
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # try:
            context = {}
            data = json.load(request)["data"]
            if "delete" in data:
                newScaleGe = EscalasEvaluaciones.objects.get(pk=data["id"])
                newScaleGe.delete()
                return JsonResponse({"message": "Deleted"})
            elif "idFind" in data:
                newScaleGe = EscalasEvaluaciones.objects.filter(pk=data["idFind"])
                findScaleGe = list(newScaleGe.values())
                childs = EscalasCalificacion.objects.filter(fk_escala_evaluacion_id=data["idFind"])
                listaChilds = list(childs.values())
                return JsonResponse({"data":findScaleGe[0], "childs":listaChilds}, safe=False)
            elif "idViejo" in data:
                newScaleGe = EscalasEvaluaciones.objects.get(pk=data["idViejo"])
            else:
                newScaleGe = EscalasEvaluaciones()
            newScaleGe.Descripcion=data["descripcion"] 
            newScaleGe.maxima_puntuacion=data["maxScore"] 
            newScaleGe.save()
            hijos = data["hijos"]
            if hijos:
                if "idViejo" in data:
                    childs = EscalasCalificacion.objects.filter(fk_escala_evaluacion=newScaleGe)
                    childs.delete()
                for newScalePa in hijos:
                    newSP = EscalasCalificacion()
                    newSP.descripcion=newScalePa["descriptionCalif"]
                    newSP.puntos_maximo=newScalePa["max_points"] 
                    newSP.fk_RangoCalificacion_id=newScalePa["quack"]
                    newSP.fk_escalaEvaluaciones= newScaleGe
                    newSP.save()      
            return JsonResponse({"message": "Perfect"})                
            # except:
            #     return JsonResponse({"message": "Error"})
                
    context = {
        "califs" : ConfTablasConfiguracion.obtenerHijos('Tipo_Calificion'),
    }
    context['segment'] = 'settings'
    html_template = (loader.get_template('scales.html'))
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def scalesGeAddModal(request): 
    context = {
        "califs" : ConfTablasConfiguracion.obtenerHijos('Tipo_Calificion'),
    }
    return render(request, 'modalAddScaleGe.html', context)
def componentTabla(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {}
        data = json.load(request)["data"]
        #Aqui cada quien puede poner su script para su tabla
        #aqui comienza la de tabla configuraciones
        if data["name"] == "tablaConfig":
            padre = data["padre"]
            hijos = ConfTablasConfiguracion.objects.filter(fk_tabla_padre=padre, mostrar_en_combos=1)
            if not hijos:
                return JsonResponse({"message":"There are no childs"})
            lista = []
            limit = None
            page = None
            #en este bucle les paso la pk de cada elemento 
            #con el fin de llamar a los metodos luego en JS
            for i in list(hijos.values()):
                i['pk'] = i['id_tabla']
                if i["maneja_lista"] == 1:
                    i["manejaLista"] = True
                    i["crearHijos"] = True
                if i["permite_cambios"] == 1:
                    i["editar"] = True
                    i["eliminable"] = True
                lista.append(i)
            if data["page"] != None and data["page"] != "":
                paginator = Paginator(lista, data["limit"])
                lista = paginator.get_page(data["page"])
                page = data["page"]
                limit = data["limit"]
            context = {
                #aqui el nombre de la columna a mostrar
                "fields": ["Description", "Actions"],
                #aqui ponemos el nombre de la columna de la BBDD
                "keys": ["desc_elemento"],
                "data": lista,
                "page": page,
                "limit": limit,
            }
        #if data["name"] == "El nombre de tu tabla"
        elif data["name"] == "tablaScales":
            hijos = EscalasEvaluaciones.objects.all()
            if not hijos:
                return JsonResponse({"message":"There are no items"})
            lista = []
            for i in list(hijos.values()):
                i['pk'] = i['id_escalaEvaluaciones']
                i['manejaLista'] = True
                i['editar'] = True
                i['eliminable'] = True
                lista.append(i)
            context = {
                
                "fields": ["Description", "Max Score", "Actions"],
                
                "keys": ["Descripcion", "maxima_puntuacion"],
                "data": lista
            }
        elif data["name"] == "tablaScalesPa":
            if "idScalesPa" in data:
                table = EscalasEvaluaciones.objects.get(pk=data["idScalesPa"])
                print(table)
                hijos = table.EscalasCalificacion_set.all()
            if not hijos:
                return JsonResponse({"message":"There are no items"})
            lista = []
            for i in list(hijos.values()):
                i['pk'] = i['id_escalaCalificacion']
                i['description_config'] = ConfTablasConfiguracion.objects.filter(id_tabla = i['fk_RangoCalificacion_id'])[0].desc_elemento
                lista.append(i)
            context = {
                
                "fields": ["Description","Qualification", "Max Score",],
                
                "keys": ["desc_calificacion","description_config", "puntos_maximo"],
                "data": lista
            }
        return render(request,'tabla.html', context)
    return