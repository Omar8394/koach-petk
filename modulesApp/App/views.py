import json

from django.http import HttpResponse, JsonResponse
from django.template import loader

from ..App.models import ConfMisfavoritos,ConfSettings,ConfSettings_Atributo,ConfTablasConfiguracion
from django.shortcuts import render
from django.template.defaulttags import register
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
    
    return render(request, "App/portalSettings.html")
def preferencias(request):
    modules=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=2,mostrar_en_combos=1)
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
                   modules=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=2,mostrar_en_combos=1)
                   dato=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=19,mostrar_en_combos=1)
                   set=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=21,mostrar_en_combos=1)
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
                    guardaset.fk_atributo_setting_id=data['data']['set']
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