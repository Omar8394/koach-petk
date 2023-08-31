from django.http import HttpResponse
from django.template import loader
from .methods import create_mail, send_mail

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
import json, math
import os
import shutil
from core import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.core.paginator import Paginator
from .models import Boletin_Info,Entrenamiento_Post,Entrenamiento_Post_Envio_personas,Entrenamiento_Post_Envio
from ..Capacitacion.models import Estructuraprograma,capacitacion_componentesXestructura,componentesFormacion
from ..App.models import ConfTablasConfiguracion,AppPublico
from .forms import BoletinForm
from django.contrib.auth.decorators import login_required
from ..Organizational_network.models import nodos_grupos 
from django.template.defaulttags import register


# from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.
@register.filter
def jsonspost(datos): 
   

  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)
  print(data['receptores'][0]['Nodos'])
  
  if data==None or data=="" or data=={}:
      return ""
  if   'receptores' in data :
     if data['receptores'][0]['Nodos']:
         return "Nodos"
     elif data['receptores'][0]['Publico']:
          return "Publico"
  else:
      return ""
# codigo para crear-actualizar-mostrar boletin-info




def createBoletin(request):
    context = {}

    tab_data = Boletin_Info.objects.all()
    
    context = {'data':tab_data}

    html_template = loader.get_template( 'Comunication/Boletin/createBoletin.html' )
    return HttpResponse(html_template.render(context, request))

def HomeViews(request):
    context={}

    profilage = Boletin_Info
    form = BoletinForm()
    
    context = {'form': form}
    html_template = loader.get_template( 'Comunication/Boletin/homeBoletin.html' )
    return HttpResponse(html_template.render(context, request))


# @api_view(['POST'])   
# @authentication_classes([])
# @permission_classes([])
# @login_required(login_url="/login/")
def addboletin(request):
    if request.method == "POST":
           
        titulo_v = request.POST.get('titulo', None)
        contenido_v = request.POST.get('contenido', None)
        path_recurso_v = request.POST.get('path_recurso', None)
        fech_inicial_v = request.POST.get('fecha_in', None)
        fech_final_v = request.POST.get('fecha_out', None)
        status_v = request.POST.get('status', None)
    
        # fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        Ruta = settings.MEDIA_ROOT + '/recursoBoletin'
        if os.path.isdir(Ruta):
            print("existe")
        else:
            
            os.mkdir(os.path.join(Ruta))

        cadena = path_recurso_v
    
        posicion=0

        while posicion != -1:
            posicion=cadena.find('src',posicion)
            if posicion != -1:
            
                cadena1=cadena[posicion+6:]
                pos_last=cadena1.index('"')
                cadena2=cadena1[:pos_last]

                cadena1=cadena2[24:]

                cadena3=cadena1.replace('/', "media/recursoBoletin/", 1)
                source= r'%s'%str(os.path.join('core/'+cadena2))
            
                destination=r'%s'%str(os.path.join('core/'+cadena3))
                
                shutil.move(source,destination)
                path_cadena=cadena2[:25]
                cadena_fin=cadena.replace(path_cadena, "media/recursoBoletin/")
                 

                posicion+=1
        
        nueva_cadena=chan_width(cadena_fin)

        ruta_ckeditor= settings.MEDIA_ROOT +"/"+ settings.CKEDITOR_UPLOAD_PATH
        # print(ruta_ckeditor)
        if os.path.isdir(ruta_ckeditor):
            # print("eliminar UPLOADS")
            shutil.rmtree(ruta_ckeditor)
            
                      
        # print(nueva_cadena)
          
        boletin = Boletin_Info.objects.create(titulo=titulo_v,contenido=contenido_v,fech_inicio=fech_inicial_v,fech_fin=fech_final_v,path_recurso=nueva_cadena,requiere_accion=1,url_accion='ninguno',status=status_v)
        boletin.save()

        return redirect('createBoletin')
        
       
def acciones_boletin(request):
    context = {}
    
    if request.method == "POST": 

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:
                
                    data = json.load(request)
                # try:                
                    if data["acceso"] == "delete":
                        
                        row_boletin = Boletin_Info.objects.get(pk=int(data["id"]))
                        row_boletin.delete()

                        return JsonResponse({"message":"okey"})

                # except:
        
                    return JsonResponse({"message":"error"}, status=500)

def edit_boletin(request, id):
    
    context = {}
    
    row_boletin = Boletin_Info.objects.get(pk=id) if id else None
    form = BoletinForm(instance=row_boletin)
    context={'form':form, 'id':id, 'data':Boletin_Info.objects.filter(pk=id)}

    html_template = (loader.get_template('Comunication/Boletin/edit_boletin_save.html'))
    return HttpResponse(html_template.render(context, request))

def edit_boletin_save(request):
    context = {}
    if request.method == "POST":
        titulo_v = request.POST.get('titulo', None)
        contenido_v = request.POST.get('contenido', None)
        path_recurso_v = request.POST.get('path_recurso', None)
        fech_inicial_v = request.POST.get('fecha_in', None)
        fech_final_v = request.POST.get('fecha_out', None)
        status_v = request.POST.get('status', None)
        idboletin_v = request.POST.get('idboletin', None)
        
        cadena_up=path_recurso_v
        for item in Boletin_Info.objects.filter(pk=idboletin_v):
            cadena_bd=item.path_recurso

        posicion=0

        
        Ruta = settings.MEDIA_ROOT+"/"+settings.CKEDITOR_UPLOAD_PATH
        if os.path.isdir(Ruta):
            print("existe")
        else:     
            
            os.makedirs(os.path.join(Ruta+str(datetime.today().strftime('%Y/%m/%d'))))
            
        
        while posicion != -1:
            posicion=cadena_bd.find('src',posicion)
            if posicion != -1:
                
                cadena1=cadena_bd[posicion+6:]
                pos_last=cadena1.index('"')
                cadena2=cadena1[:pos_last]

                cadena3=cadena2.replace('media/recursoBoletin', "media/uploads/"+str(datetime.today().strftime('%Y/%m/%d')), 1)
                # print(cadena3)
                    
                    
                source= r'%s'%str(os.path.join('core'+cadena2))
                    
                destination=r'%s'%str(os.path.join('core'+cadena3))
                        
                shutil.move(source,destination)
                    
                    
                posicion+=1
            
            
        posicion=0
        while posicion != -1:
            posicion=cadena_up.find('src',posicion)
            if posicion != -1:
                
                cadena1=cadena_up[posicion+6:]
                pos_last=cadena1.index('"')
                cadena2=cadena1[:pos_last]

                    
                cadena3=cadena2.replace('media/recursoBoletin', "media/uploads/"+str(datetime.today().strftime('%Y/%m/%d')), 1)
                # print(cadena3)

                cadena1=cadena3[24:]

                cadena4=cadena1.replace('/', "media/recursoBoletin/", 1)
                source= r'%s'%str(os.path.join('core'+cadena3))
                
                destination=r'%s'%str(os.path.join('core'+cadena4))
                    
                shutil.move(source,destination)
                path_cadena=cadena3[:25]
                path_recurso_v=cadena_up.replace(path_cadena, "media/recursoBoletin/")
                    

                posicion+=1


        ruta_ckeditor= settings.MEDIA_ROOT+"/"+settings.CKEDITOR_UPLOAD_PATH
        
        if os.path.isdir(ruta_ckeditor):
            
            shutil.rmtree(ruta_ckeditor)
        # print(path_recurso_v)

        nueva_cadena=chan_width(path_recurso_v)

        boletin = Boletin_Info.objects.get(pk=idboletin_v)

        boletin.titulo=titulo_v
        boletin.contenido=contenido_v
        boletin.fech_inicio=fech_inicial_v
        boletin.fech_fin=fech_final_v
        boletin.path_recurso=nueva_cadena
        boletin.requiere_accion=0
        boletin.url_accion='ninguno'
        boletin.status=status_v


        boletin.save()

        return redirect('createBoletin')
                
def chan_width(cadena):
    posicion=0
    while posicion != -1:
            posicion=cadena.find('width',posicion)
            if posicion != -1:
                
                cadena1=cadena[posicion:]
                pos_last=cadena1.index('px')
                cadena2=cadena1[:pos_last]
                cadena=cadena.replace(cadena2, "width:390") 
                    
                posicion+=1

    return(cadena)
        

              

def showBoletin(request):
    context = {'data': Boletin_Info.objects.all()}

    if request.method == "POST": 

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:

                html_template = loader.get_template( 'Comunication/Boletin/showBoletin.html' )
                return HttpResponse(html_template.render(context, request))

# endblock boletin-info

def emailTest(request):
    context = {"titulo": "Account Registration Link", "user": "publico.nombre" + " " + "publico.apellido",
                                "content": "Thank you for joining the " + 
                                    "settings.EMPRESA_NOMBRE" + " team, follow the link below to register  your account:",
                                "enlace": "enlace", "enlaceTexto": "click here!", "empresa": "settings.EMPRESA_NOMBRE",
                                "urlimage": "settings.EMPRESA_URL_LOGO"}
    send_mail(create_mail("tadifred@gmail.com", "Account Registration Link", "base_email_template_pro.html",
                                        context))
    return HttpResponse("fine")
def Registro_enviopost(request):
    
    context = {}
    html_template = loader.get_template( 'registroPost.html' )
    return HttpResponse(html_template.render(context, request))
def modalAddenvios(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                
                print(data)
                if data['method'] == "Show":
                    escuela=Estructuraprograma.objects.filter(valor_elemento='Process')
                    context = {'escuela':escuela}
                    html_template = (loader.get_template('ModalAddenvio.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data['method'] == "Editar":
                     edita=Entrenamiento_Post.objects.get(pk=data['pk'])
                     escuela=Estructuraprograma.objects.filter(valor_elemento='Process')
                     context = {'edita':edita,'escuela':escuela}
                     html_template = (loader.get_template('ModalAddenvio.html'))
                     return HttpResponse(html_template.render(context, request))
                elif data['method'] == "Create":
                     print(data)
                     save_post=Entrenamiento_Post.objects.create()
                     save_post.link_post=data['data']['descriptionActivity']
                     save_post.fk_escuela_id=data['data']['Escuela']
                     save_post.fk_modulo_id=data['data']['Modulo']
                     save_post.fk_topico_id=data['data']['estatusLesson']
                     save_post.orden=len(Entrenamiento_Post.objects.all()) + 1
                     save_post.save()
                     return JsonResponse({"message":"ok"})
                elif data['method'] == 'Update':
                     print(data)  
                     edita_post=Entrenamiento_Post.objects.get(pk=data['id'])
                     edita_post.link_post=data['data']['descriptionActivity']
                     edita_post.fk_escuela_id=data['data']['Escuela']
                     edita_post.fk_modulo_id=data['data']['Modulo']
                     edita_post.fk_topico_id==data['data']['estatusLesson']                    
                     edita_post.save()
                     return JsonResponse({"message":"ok"}) 
                elif data["method"] == "sort":
                     print(data)
                     paginas=Entrenamiento_Post.objects.all()
                     i = 1
                     for d in data['data']:
                         if d != None:
                            pagina = paginas.get(id_post=d)
                            pagina.orden = i
                            i = i + 1
                            pagina.save()
                     return JsonResponse({"message":"ok"}, status=200)
                elif data['method'] == 'Delete':
                     print(data)  
                     delete_post=Entrenamiento_Post.objects.get(pk=data['id'])
                     delete_post.delete()
                     return JsonResponse({"message":"ok"})  
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def RenderPost(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                lista=[]
                if data["query"] == "":
                   grupos=Entrenamiento_Post.objects.all().order_by('orden')
                   
                   paginator = Paginator(grupos, data["limit"])
                   lista = paginator.get_page(data["page"])
                   page = data["page"]
                   limit = data["limit"]      
                  
                   context = {"grupos":grupos,"page": page,"limit": limit,'data':lista}
                   html_template = (loader.get_template('renderPost.html'))
                   return HttpResponse(html_template.render(context, request)) 
                           
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)        
def programar_post(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                lista=[]
                if data["query"] == "":
                   programar='' 
                   programado=Entrenamiento_Post_Envio.objects.all() 
                   if programado.exists():
                      programar=programado[0] 
                   frecuencia=ConfTablasConfiguracion.obtenerHijos('Ritmo_Capacitacion')
                   context = {'frecuencia':frecuencia,'programado':programar}
                   print(context)
                   html_template = (loader.get_template('Post_envio.html'))
                   return HttpResponse(html_template.render(context, request)) 
                elif data['query'] == "Save":
                    
                   programado=Entrenamiento_Post_Envio.objects.all() 
                   if programado.exists():
                    programado.delete()
                    programar=[]
                    datosjson=""
                    obj={}
                    datos = {}
                    if data['tipo']=='publico':                   
                       obj["Nodos"]="" 
                       obj["Publico"]=data['receptores']            
                    
                       programar.append(obj or 0)
                       datos['receptores']=programar
                       print(data)                  
                    elif data['tipo'] =='nodos':  
                       obj["Nodos"]=data['receptores'] 
                       obj["Publico"]=""            
                    
                       programar.append(obj or 0)
                       datos['receptores']=programar
                       print(data)
                    
                    todos=Entrenamiento_Post.objects.all()
                    for item in todos:
                        post=Entrenamiento_Post_Envio.objects.create()
                        post.fk_post_id=item.id_post
                        post.tipo_recordatorio_id=data['tiempo']
                        post.tiempo_recordatorio=data['reps']
                        post.tipo_receptor=json.dumps(datos)
                        post.save()
                    return JsonResponse({"message":"ok"})
                   else:
                    programar=[]
                    datosjson=""
                    obj={}
                    datos = {}
                    if data['tipo']=='publico':                   
                       obj["Nodos"]="" 
                       obj["Publico"]=data['receptores']            
                    
                       programar.append(obj or 0)
                       datos['receptores']=programar
                       print(data)                  
                    elif data['tipo'] =='nodos':  
                       obj["Nodos"]=data['receptores'] 
                       obj["Publico"]=""            
                    
                       programar.append(obj or 0)
                       datos['receptores']=programar
                       print(data)
                    
                    todos=Entrenamiento_Post.objects.all()
                    for item in todos:
                        post=Entrenamiento_Post_Envio.objects.create()
                        post.fk_post_id=item.id_post
                        post.tipo_recordatorio_id=data['tiempo']
                        post.tiempo_recordatorio=data['reps']
                        post.tipo_receptor=json.dumps(datos)
                        post.save()
                    return JsonResponse({"message":"ok"})             
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def renderTipocombo(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                print(data)
                lista=[]
                if data["tipo"] == "Publico":
                   publico=AppPublico.objects.all()
                   paginator = Paginator(publico, data["limit"])
                   lista = paginator.get_page(data["page"])
                   page = data["page"]
                   limit = data["limit"]
                   context = {"page": page,"limit": limit,'publico':publico,'data':lista}
                   html_template = (loader.get_template('Tiporeceptor.html'))
                   return HttpResponse(html_template.render(context, request)) 
                elif data["tipo"]== "Nodos" :
                   grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,status_grupo=60)
                   print(grupos)
                   context = {'grupo':grupos}
                   html_template = (loader.get_template('rendercomboreceptor.html'))
                   return HttpResponse(html_template.render(context, request))           
                elif data['query'] == "Hijos":
                    print(data)
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=data['pk'])
                    print(grupos)
                    if grupos.exists():
                        
                       context = {'grupo':grupos}
                    else:
                       hijo=nodos_grupos.objects.filter(if_gruponodo=data['pk'])
                       context = {'grupo':hijo,'elegido':hijo[0]}
                    html_template = (loader.get_template('rendercomboreceptor.html'))
                    return HttpResponse(html_template.render(context, request))
               
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                   