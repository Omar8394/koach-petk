import json, math
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.template import loader
import sys
from ..App.models import ConfMisfavoritos,ConfSettings,ConfSettings_Atributo,ConfTablasConfiguracion,AppPublico
from ..Capacitacion.models import EscalasEvaluaciones,EscalasCalificacion
from django.shortcuts import render
from django.template.defaulttags import register
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
import datetime
from ..Security.models import User,Log_Transacciones
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
# Create your views here.
TITULOPUBLIC = {'idpublico':'#', 'nombre': 'Usuario',  'telefono_principal': 'Telefono Principal', 'correo_principal': 'Email Principal', 'Rol_usuario': 'Rol'}
@register.filter
def get_attr(dictionary, key):
    return(getattr(dictionary, key))

@register.filter
def get_list(dictionary, key):
    return dictionary[key-1]

@register.filter
def replaces(value, key):
    txt = re.search(key, value, flags = re.IGNORECASE)
    print(txt)
    return re.sub(key, '<b style="background-color:#c0ffc8;">%s</b>' %txt[0], value, flags = re.IGNORECASE, count =1)

@register.filter
def matches(value, key):
    return re.search(key, value, flags = re.IGNORECASE) != None

@register.filter
def tostring(value):
    return str(value)
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
@register.filter
def tostringJson(value, key):
    try:
        txt = json.loads(value)
        return txt[key] if txt[key] else ""
    except:
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
@login_required(login_url="/security/login/") 
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
                print(data)
                newScaleGe = EscalasEvaluaciones.objects.filter(pk=data["idFind"])
                findScaleGe = list(newScaleGe.values())
                print(findScaleGe)
                childs = EscalasCalificacion.objects.filter(fk_escalaEvaluaciones_id=data["idFind"])
                listaChilds = list(childs.values())
                print(listaChilds)
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
                    childs = EscalasCalificacion.objects.filter(fk_escalaEvaluaciones=newScaleGe)
                    childs.delete()
                for newScalePa in hijos:
                    newSP = EscalasCalificacion()
                    newSP.descripcion=newScalePa["descriptionCalif"]
                    newSP.puntos_maximo=newScalePa["max_points"] 
                    newSP.fk_RangoCalificacion=ConfTablasConfiguracion.objects.get(desc_elemento=newScalePa["quack"])
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


@login_required(login_url="/security/login/") 
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
            print(hijos)
            if not hijos:
                return JsonResponse({"message":"There are no childs"})
            lista = []
            limit = None
            page = None
            #en este bucle les paso la pk de cada elemento 
            #con el fin de llamar a los metodos luego en JS
            for i in list(hijos.values()):
                i['pk'] = i['id_tabla']
                if i["Maneja_lista"] == 1:
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
                print(data)
                table = EscalasEvaluaciones.objects.get(pk=data["idScalesPa"])
                print(table)
                hijos = EscalasCalificacion.objects.filter(fk_escalaEvaluaciones=table)
            if not hijos:
                return JsonResponse({"message":"There are no items"})
            lista = []
            for i in list(hijos.values()):
                i['pk'] = i['id_escalaCalificacion']
                i['description_config'] = ConfTablasConfiguracion.objects.filter(id_tabla = i['fk_RangoCalificacion_id'])[0].desc_elemento
                lista.append(i)
            context = {
                
                "fields": ["Description","Qualification", "Max Score",],
                
                "keys": ["descripcion","description_config", "puntos_maximo"],
                "data": lista
            }
            print(context)
        return render(request,'tabla.html', context)
    return
def managepersons(request):
    search_query = request.GET.get('search_box', "")
    program = AppPublico.objects.all()
    return render(request,"manage_persons.html",{'plan': paginas(request, program), 'keys' : TITULOPUBLIC, 'urlEdit': 'unlockPublic', 'urlRemove': 'lockPublic', 'search':search_query, 'tipo':'Public', 'segment':'settings'}) 
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

def unlockPublic(request):
    print(request.user.pk)
    # code = str(Methods.getVerificationLink(request.user.email, 1))

    if request.method == "POST":  

        try:

            id=request.POST.get('id')

            ctauserPu = AppPublico.objects.get(idpublico=id).user_id_id
            ctauser=User.objects.filter(pk=ctauserPu)

            ctauser.update(fk_status_cuenta_id= ConfTablasConfiguracion.objects.get(valor_elemento='user_active').id_tabla)

            # messages.info(request, 'Public Unlocked Successfully')
            return JsonResponse({"mensaje" : "exito"})

        except:

            return JsonResponse({"mensaje" : "Error, try again later"})
def lockPublic(request):
    print(request.user.pk)
    if request.method == "POST":  

        try:

            id=request.POST.get('id')
            ctauserPu = AppPublico.objects.get(idpublico=id).user_id_id
            ctauser=User.objects.filter(pk=ctauserPu)
            if str(request.user.pk) != str(id) and ctauser[0].fk_status_cuenta.valor_elemento != 'status_verification':
                print(request.user.pk)
                ctauser.update(fk_status_cuenta_id= ConfTablasConfiguracion.objects.get(valor_elemento='user_account_blocked').id_tabla)
                # messages.info(request, 'Public Locked Successfully')
                return JsonResponse({"mensaje" : "exito"})

            else:

                return JsonResponse({"mensaje" : "self" if ctauser[0].fk_status_cuenta.valor_elemento != 'status_verification' else 'verification'})


        except:

            return JsonResponse({"mensaje" : "Error, try again later"})
def listaRol(request):
    
    if request.method == "POST":  

        id = request.POST.get('id', None)
        users= AppPublico.objects.get(user_id_id=request.user.pk)
        if str(users.pk) != str(id):

            publico = AppPublico.objects.get(idpublico=id)

            if publico and publico.nombre:

                extension = AppPublico.objects.get(pk=publico.pk)

                if extension and extension.user_id:

                    roles = ConfTablasConfiguracion.obtenerHijos('Roles')
                    html = render_to_string('listaRoles.html', {'lista': roles, 'activo': extension.user_id.fk_rol_usuario.desc_elemento})
                    return JsonResponse({'html': html}) 

                else:

                    return JsonResponse({'html': 'noUser'}) 

            else:

                return JsonResponse({'html': 'noPublic'}) 
        else:

            return JsonResponse({'html': 'self'}) 

def setRole(request):
    
    if request.method == "POST":  

        id = request.POST.get('id', None)
        rol = request.POST.get('rol', None)
        publico = AppPublico.objects.get(idpublico=id)
        cuenta = User.objects.get(pk=publico.pk)
        cuenta.fk_rol_usuario = ConfTablasConfiguracion.objects.get(id_tabla=rol)
        cuenta.save()
        log=Log_Transacciones.objects.create()
        log.fecha_transaccion=datetime.datetime.now()
        log.fk_transaccion_id=ConfTablasConfiguracion.objects.get(valor_elemento="Cambio_rol").pk
        log.fk_Cta_usuario=request.user
        log.save()
        return JsonResponse({'html': 'self'}) 
def paginar(request):
    
    public = request.POST.get('id', None)
    tipo = request.POST.get('tipo', None)
    filtro = request.POST.get('filtro', None)
    orden = request.POST.get('orden', None)
    tipoOrden = request.POST.get('tipoOrden', "")
    fecha1 = request.POST.get('fecha1', None)
    fecha2 = request.POST.get('fecha2', None)
    rango = request.POST.get('rango', None)

    if tipo and tipo == 'Public':
        
        plan = AppPublico.objects.all()
        # extension = ExtensionUsuario.objects.select_related().all()
        # for ext in extension:
        #     if ext.CtaUsuario:
        #         print(ext.Publico.nombre)

   

    if filtro:

        filtro = filtro.strip()

       
        if tipo and tipo == 'Public':
            
            plan = plan.filter(Q(idpublico__icontains=filtro) | Q(user_id__username__icontains=filtro) | Q(user_id__fk_rol_usuario__desc_elemento__icontains=filtro) | Q(correo_principal__icontains=filtro) | Q(telefono_principal__icontains=filtro) | Q(user_id__fk_status_cuenta__desc_elemento__icontains=filtro))
            
       
   
    if(orden):

        plan = plan.order_by(tipoOrden + orden)



    # test = Perfil.objects.get(idperfil=55)
    # print(getattr(test, 'idperfil'))
    # # print(pagina)
    
    
    if tipo and tipo == 'Public':

        pagina = render_to_string('paginas.html', {'plan': paginas(request, plan, rango)})
        tabla = render_to_string('contenidoTablaPublic.html', {'plan': paginas(request, plan, rango), 'keys' : TITULOPUBLIC, 'urlEdit': 'unlockPublic', 'urlRemove': 'lockPublic', 'search':filtro, 'orden':orden, 'tipoOrden': tipoOrden, 'tipo': 'Public'})

    

    response = {
        'paginas': pagina,
        'contenido' : tabla
    }

    return JsonResponse(response)                