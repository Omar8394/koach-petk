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

from .models import Boletin_Info
from .forms import BoletinForm
from django.contrib.auth.decorators import login_required
# from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

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
                print(cadena3)
                    
                    
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
                print(cadena3)

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