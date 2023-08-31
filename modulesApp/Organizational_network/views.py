from django.shortcuts import render
from ..App.models import ConfTablasConfiguracion,AppPublico
from ..Capacitacion.models import Estructuraprograma, capacitacion_ActSesiones_programar, capacitacion_Actividad_Sesiones, capacitacion_Actividad_leccion, capacitacion_Actividad_tareas, capacitacion_ComponentesActividades, capacitacion_EvaluacionesPreguntas, capacitacion_EvaluacionesPreguntasOpciones, capacitacion_LeccionPaginas, capacitacion_Recursos,capacitacion_componentesXestructura,componentesFormacion,capacitacion_Tag,capacitacion_TagRecurso,capacitacion_componentesPrerequisitos,EscalasEvaluaciones,capacitacion_ActividadEvaluaciones,capacitacion_EvaluacionesBloques,capacitacion_ActividadesTiempoReal,capacitacion_Examenes,capacitacion_ExamenesResultado,capacitacion_NotificacionesMensajesXactividad,capacitacion_HistoricoActividades
from ..Organizational_network.models import nodos_grupos,nodos_gruposIntegrantes,nodos_PlanFormacion
from ..Comunication.models import Comunication_MsjPredeterminado,Boletin_Info 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template import loader
from django.template.loader import render_to_string
from django.template.defaulttags import register
import time, json
import datetime
from django.db.models import Q
from django.db.models import F, FloatField
from django.db.models import Count
from django.db.models import Max
from django.core.paginator import Paginator
# Create your views here.
@register.filter
def Hijos(name):
    print(name)
    padre=nodos_grupos.objects.get(valor_elemento=name).pk
    hijos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=padre)
    print(hijos)
    return hijos
@register.filter
def verificar_inscripcion(integrante):
    integrante_valido=nodos_gruposIntegrantes.objects.filter(fk_public_id=integrante,status_integrante=ConfTablasConfiguracion.objects.get(valor_elemento='Status_activo')) 
    if integrante_valido.exists():
       integrante_valido 
    return integrante_valido 
@register.filter
def verifi_integrante(integrante,grupo):
    print(grupo)
    integrante=nodos_gruposIntegrantes.objects.filter(fk_public_id=integrante,fk_nodogrupo_id=grupo) 
    print(integrante)
    if integrante.exists():
       integrante
       
    return integrante
@register.filter
def verifis(integrante):
    
    integrante=nodos_gruposIntegrantes.objects.filter(fk_public_id=integrante) 
    print(integrante)
    if integrante.exists():
       integrante
       
    return integrante
@register.filter
def grupos_mundo(pais):
    print(pais) 
    verdad=False 
    paises=ConfTablasConfiguracion.objects.filter(valor_elemento=pais)
    print(paises)
    if paises.exists():
       Grupo=nodos_grupos.objects.filter(ubicacion=paises)
       if Grupo.exists():
          verdad=True 
       else:
          verdad=False
    return verdad          
def index_nodos(request):
    user = request.user
    rol=user.fk_rol_usuario 
    paises = request.GET.get("id" or None)
    print(paises)
    context = {'paises':paises}
   
    if str(rol) == "Admin"  or str(rol) == "Lider":
       html_template = (loader.get_template('grupos_nodos.html'))
    else:
        html_template = (loader.get_template('page-403.html'))
    return HttpResponse(html_template.render(context, request))
def modalAddgrupos(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:    
                data = json.load(request)
                
                print(data)
                if data['method'] == "Show":
                    status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                    ponente=AppPublico.objects.filter(user_id__fk_rol_usuario_id=110)
                    ubicacion=ConfTablasConfiguracion.obtenerHijos(valor="countries_iso")
                    context = {'status':status,'ubicacion':ubicacion,'ponente':ponente}
                    html_template = (loader.get_template('ModalAddgrupopadre.html'))
                    return HttpResponse(html_template.render(context, request))
                elif data['method'] == "Editar":
                     print(data)
                     grupos=nodos_grupos.objects.get(pk=data['pk'])
                     status = ConfTablasConfiguracion.obtenerHijos(valor="Status_global")
                     ponente=AppPublico.objects.filter(user_id__fk_rol_usuario_id=110)
                     ubicacion=ConfTablasConfiguracion.obtenerHijos(valor="countries_iso")
                     context = {'grupos':grupos,'status':status,'ubicacion':ubicacion,'ponente':ponente}
                     html_template = (loader.get_template('ModalAddgrupopadre.html'))
                     return HttpResponse(html_template.render(context, request))
                elif data['method'] == "Create":
                     print(data)
                     Grupos=nodos_grupos.objects.create()
                     Grupos.Descripcion=data['data']['descriptionActivity']
                     Grupos.valor_elemento=data['data']['urlActivity']
                     Grupos.fecha_creacion=data['data']['disponibleLesson']
                     Grupos.fk_liderGrupo_id=data['data']['Director']
                     Grupos.status_grupo_id=data['data']['estatusLesson']
                     Grupos.ubicacion_id=data['data']['Ubicacion']
                     
                     Grupos.save()
                     return JsonResponse({"message":"ok"})
                elif data['method'] == 'Delete':
                     grupos=nodos_grupos.objects.get(pk=data['id'])
                     grupos.fk_grupoNodo_padre=nodos_grupos.objects.get(valor_elemento='grupo_papelera')
                     grupos.save()
                     return JsonResponse({"message":"delete"})
                elif data['method'] == 'Update':
                     print(data)
                     if data['tipo']=='guarda_hijos':
                        Grupos=nodos_grupos.objects.create()
                        Grupos.Descripcion=data['data']['descriptionActivity']
                        Grupos.valor_elemento=data['data']['urlActivity']
                        Grupos.fecha_creacion=data['data']['disponibleLesson']
                        Grupos.fk_liderGrupo_id=data['data']['Director']
                        Grupos.status_grupo_id=data['data']['estatusLesson']
                        Grupos.ubicacion_id=data['data']['Ubicacion']
                        Grupos.fk_grupoNodo_padre_id=data['id']
                        Grupos.save()
                     elif data['tipo']  == 'edita_padres': 
                        Grupos =nodos_grupos.objects.get(pk=data['id'])
                        Grupos.Descripcion=data['data']['descriptionActivity']
                        Grupos.valor_elemento=data['data']['urlActivity']
                        Grupos.fecha_creacion=data['data']['disponibleLesson']
                        Grupos.fk_liderGrupo_id=data['data']['Director']
                        Grupos.status_grupo_id=data['data']['estatusLesson']
                        Grupos.ubicacion_id=data['data']['Ubicacion'] 
                        Grupos.fk_grupoNodo_padre_id=None                 
                        Grupos.save()
                     elif data['tipo']  == 'edita_hijos':
                        Grupos =nodos_grupos.objects.get(pk=data['id'])
                        Grupos.Descripcion=data['data']['descriptionActivity']
                        Grupos.valor_elemento=data['data']['urlActivity']
                        Grupos.fecha_creacion=data['data']['disponibleLesson']
                        Grupos.fk_liderGrupo_id=data['data']['Director']
                        Grupos.status_grupo_id=data['data']['estatusLesson']
                        Grupos.ubicacion_id=data['data']['Ubicacion'] 
                                       
                        Grupos.save()  
                     return JsonResponse({"message":"ok"})
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)        
def renderGrupoPadre(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                page=''
                limit=''
                data = json.load(request)
                print(data)
                lista=[]
                if data["query"] == "":
                   if data['idpa'] == 'None':
                    print('hola')   
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,status_grupo=60)
                    if grupos.exists():
                       paginator = Paginator(grupos, data["limit"])
                       lista = paginator.get_page(data["page"])
                       page = data["page"]
                       limit = data["limit"]
                    else:
                        title = True   
                   else: 
                    pais= ConfTablasConfiguracion.objects.get(valor_elemento=data['idpa'])  
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,ubicacion=pais,status_grupo=60)
                    if grupos.exists():
                       paginator = Paginator(grupos, data["limit"])
                       lista = paginator.get_page(data["page"])
                       page = data["page"]
                       limit = data["limit"]      
                    else:
                       title = True  
                   context = {"grupos":grupos,"page": page,"limit": limit,'data':lista,'title':title}
                   html_template = (loader.get_template('renderGruposPadre.html'))
                   return HttpResponse(html_template.render(context, request))           
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)          
def renderHijos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "hijos":
                    padre=nodos_grupos.objects.get(pk=data['pk'])
                    print(padre.pk)
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=padre.pk)
                    print(grupos)
                    if grupos.exists():
                       context = {"grupos":grupos}
                    html_template = (loader.get_template('renderHijos.html'))
                    return HttpResponse(html_template.render(context, request))           
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)                    
def Grupos_integrantes(request, elemento):
    grupo=nodos_grupos.objects.get(valor_elemento=elemento) 
    integrantes=AppPublico.objects.filter(pais=grupo.ubicacion, user_id__fk_rol_usuario=ConfTablasConfiguracion.objects.get(valor_elemento="Interesado") )
    idPersona=None
    is_cookie_set = 0
    if 'idPersona' in request.session:
        idPersona=request.session['idPersona'] if 'idPersona' in request.session else None  
        is_cookie_set = 1
    if request.method == "GET":
       if request.GET.get('page')==None: 
          is_cookie_set = 0 
          request.session['idPersona']=None
          idPersona=None
       if (is_cookie_set == 1):
          if idPersona!=None and idPersona!="":
              integrantes=integrantes.filter(nombre__icontains=idPersona)
    if request.method == "POST":
        print('hola')        
        if (is_cookie_set == 1):          
          request.session['idPersona']=None 
        idPersona=request.POST.get('PersonId')
        print(request.POST)
        if idPersona != None and idPersona!="" :
            
           integrantes=integrantes.filter(nombre__icontains=idPersona) 
           request.session['PersonId'] = idPersona             
    paginator = Paginator(integrantes, 10)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'matriculasList': page_obj,'elemento':elemento,'integrantes':integrantes,'gruposi':grupo.pk,'titulo':grupo.Descripcion}
    html_template = (loader.get_template('integrantes.html'))
    return HttpResponse(html_template.render(context, request))   
def plan_nodo(request, grupo):
    grupo=nodos_grupos.objects.get(valor_elemento=grupo) 
    componentes=capacitacion_componentesXestructura.objects.all()
    
    context = {'gruposi':grupo.pk,'componentes':componentes,'titulo':grupo.Descripcion}
    html_template = (loader.get_template('plan_grupo.html'))
    return HttpResponse(html_template.render(context, request))
def getcomponentsxplan(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                title=False
                lista=[]
                if data["query"] == "": 
                   componentes=nodos_PlanFormacion.objects.filter(fk_gruponodo_id=data["id"])
                   if componentes.exists():
                      paginator = Paginator(componentes, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"] 
                      context = {"componentes":componentes,"page": page,"limit": limit,'data':lista}
                      html_template = (loader.get_template('Plan_relation.html')) 
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"title":title}
                      html_template = (loader.get_template('Plan_relation.html')) 
                      return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def getestru_components(request):
    if request.method == "POST":
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                title=False
                lista=[]
                if data["query"] == "": 
                   componentes=capacitacion_componentesXestructura.objects.all()
    
                   if componentes.exists():
                      paginator = Paginator(componentes, data["limit"])
                      lista = paginator.get_page(data["page"])
                      page = data["page"]
                      limit = data["limit"] 
                      context = {"componentes":componentes,"page": page,"limit": limit,'data':lista}
                      html_template = (loader.get_template('renderestruplan.html')) 
                      return HttpResponse(html_template.render(context, request))
                   else:
                      title=True
                      context = {"title":title}
                      html_template = (loader.get_template('renderestruplan.html')) 
                      return HttpResponse(html_template.render(context, request))
        except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)           
def Saveestrutura_plan(request) :  
    estructura=request.POST.get('estructura') 
    id=request.POST.get('id')
    print(id)
    notsave=nodos_PlanFormacion.objects.filter(fk_componentesXestructura_id=estructura,fk_gruponodo_id=id)
    if notsave.exists():
       return JsonResponse({"message":"no"})
    else:
       componente=nodos_PlanFormacion()
       componente.fk_componentesXestructura_id=estructura
       componente.fk_gruponodo_id=id
       componente.fecha_inicio=datetime.datetime.now()
       componente.fk_statusplan=ConfTablasConfiguracion.objects.get(valor_elemento='Status_activo')
       componente.orden_presentacion=len(nodos_PlanFormacion.objects.filter(fk_gruponodo_id=id)) + 1
       componente.save()
       return JsonResponse({"message":"ok"})
def saveintegrantes(request):
    if request.method == "POST":
       estructura=request.POST.get('padr')
       grupo=request.POST.get('grupo')
       #resul=json.load(request)
       print(request.POST)
       print(grupo)
       print('User count:', len(json.loads(estructura)))
      
       x=0 
       #print(json.loads(estructura)["clave" + str(1)] )
       
       for key in json.loads(estructura):
           idmatricla=json.loads(estructura)["clave" + str(x)]
           integrantes_viejos=nodos_gruposIntegrantes.objects.filter(fk_nodogrupo_id=grupo,fk_public_id= idmatricla) 
           if not integrantes_viejos.exists():
               
              saveintegrantes=nodos_gruposIntegrantes.objects.create()
              saveintegrantes.fk_nodogrupo_id=grupo
              saveintegrantes.fk_public_id= idmatricla
              saveintegrantes.fecha_incorporacion=datetime.datetime.now()
              saveintegrantes.status_integrante=ConfTablasConfiguracion.objects.get(valor_elemento='Status_activo')
              
              saveintegrantes.save()
           else:
              integrantesviejos=nodos_gruposIntegrantes.objects.get(fk_nodogrupo_id=grupo,fk_public_id= idmatricla)   
              integrantesviejos.status_integrante=ConfTablasConfiguracion.objects.get(valor_elemento='Status_activo')
              integrantesviejos.motivo_desincorporacion=None
              integrantesviejos.save()
           x+=1
       
      
        
       
       data = json.dumps({'status': 'OK'})
       return HttpResponse(data, content_type="application/json", status=200)     
def ModalAdddatos(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    datos=nodos_gruposIntegrantes.objects.get(fk_public_id=data['integra'],fk_nodogrupo_id=data['grupo_id'])
                    context = {'datos':datos}
                    html_template = (loader.get_template('modalAdddatos.html'))
                    return HttpResponse(html_template.render(context, request))           
                elif data['method'] == "Create":
                     print(data)
                     grupo_integra=nodos_gruposIntegrantes.objects.get(fk_public=data['tipo'],fk_nodogrupo_id=data['id'])
                     grupo_integra.datos_adicionales=data['data']['resumen']
                     grupo_integra.descripcion_comentarios=data['data']['resumendatos']
                     grupo_integra.save()
                     return JsonResponse({"message":"ok"}) 
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)    
def ModalStatus(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    datos=nodos_gruposIntegrantes.objects.get(fk_public_id=data['integra'],fk_nodogrupo_id=data['grupo_id'])
                    context = {'datos':datos}
                    html_template = (loader.get_template('modalStatus.html'))
                    return HttpResponse(html_template.render(context, request))           
                elif data['method'] == "Create":
                     print(data)
                     grupo_integra=nodos_gruposIntegrantes.objects.get(fk_public=data['tipo'],fk_nodogrupo_id=data['id'])
                     if 'checkDurationC' in data['data']:
                        grupo_integra.status_integrante=ConfTablasConfiguracion.objects.get(valor_elemento='Status_inactivo')
                        grupo_integra.motivo_desincorporacion_id=data['data']['resumen']
                        grupo_integra.save()
                     return JsonResponse({"message":"ok"})
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)    
def renderstat(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    motivo=ConfTablasConfiguracion.obtenerHijos('Motivo_Desincorpora')
                    context = {'motivo':motivo}
                    html_template = (loader.get_template('rendermotivo.html'))
                    return HttpResponse(html_template.render(context, request)) 
               
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)
def Modaltransfer(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    print(data)
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,status_grupo=60)
                    context = {'grupos':grupos}
                    html_template = (loader.get_template('modaltransfer.html'))
                    return HttpResponse(html_template.render(context, request)) 
                elif data['method'] == "Create":
                     print(data)
                     grupo_transfer=nodos_gruposIntegrantes.objects.get(fk_public=data['tipo'])
                     grupo_transfer.fk_nodogrupo_id=data['data']['categoryProgram']
                     grupo_transfer.save()
                     return JsonResponse({"message":"ok"})
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)    
def RenderListas(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                
                if data["method"] == "Show":
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
def mapamundi_nodos(request): 
    context = {}
    html_template = (loader.get_template('Vernodos_mapa.html'))
    return HttpResponse(html_template.render(context, request)) 
def Modalverpais(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    print(data)
                    inte=0
                    pais=ConfTablasConfiguracion.objects.filter(fk_tabla_padre=ConfTablasConfiguracion.objects.get(valor_elemento='countries_iso'),valor_elemento=data['id'])
                    if pais.exists():
                       nodos=nodos_grupos.objects.filter(ubicacion=pais[0])
                       for item in nodos:
                           integrantes=nodos_gruposIntegrantes.objects.filter(fk_nodogrupo__fk_grupoNodo_padre=item)
                           if integrantes.exists():
                              inte=integrantes.count()
                                                       
                       context = {'pais':pais[0],'inte':inte,'data':data['id'],'nodos':nodos.count()}
                    else:
                       
                       context={'pais':'No Disponible','inte':'No Disponible','nodos':'No Disponible'}
                    html_template = (loader.get_template('modalverpais.html'))
                    return HttpResponse(html_template.render(context, request)) 
               
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500) 
def grupos_mundo(request):
    paise = request.POST.get("pais")
    print(paise)
    data=[] 
    paises=ConfTablasConfiguracion.objects.filter(valor_elemento=paise)
    
    if paises.exists():
       Grupo=nodos_grupos.objects.filter(fk_grupoNodo_padre=None,ubicacion=paises[0])
       if Grupo.exists():
          data = json.dumps({'status': 'OK'}) 
         
       else:
          data = json.dumps({'status': 'VO'})
    return HttpResponse(data, content_type="application/json", status=200)
    
   
                       
# def MatriculacionAdmintwo(request):
#     cta=ExtensionUsuario.objects.get(user=request.user).CtaUsuario
#     if cta.fk_rol_usuario.valor_elemento != 'rol_admin':
#       return HttpResponseForbidden()

  
#     msg = None
#     vari='""'
#     #matriculaList=MatriculaAlumnos.objects.all()
#     matriculaList=MatriculaAlumnos.objects.annotate(tipoTest=F('fk_publico__extensionusuario__CtaUsuario__sponsor_code')).all().order_by('fk_publico__apellido')
#     #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE appu.procedencia =%s"%(vari))
#     print(matriculaList.query)
#     status=TablasConfiguracion.obtenerHijos("EstMatricula")
#     types=TablasConfiguracion.obtenerHijos("Tipo Matricula")
#     sponsor=Partners.objects.all().exclude(nombre_empresa="").exclude(nombre_empresa=None)


#     fechaF=None
#     fechaI=None
#     idOrigen=None
#     idPersona=None
#     idStatus=None
#     idTipo=None
#     idSponsor=None

#     personaBuscarNombre=None



    

#     is_cookie_set = 0
   
#     if 'fechaInicial' in request.session or 'fechaFinal' in request.session or 'idPersona' in request.session or 'idStatus' in request.session or 'idTipo' in request.session  or 'idOrigen' in request.session : 
#         fechaF = request.session['fechaFinal'] if 'fechaFinal' in request.session else None
#         fechaI = request.session['fechaInicial'] if 'fechaInicial' in request.session else None
#         idPersona=request.session['idPersona'] if 'idPersona' in request.session else None
#         idStatus=request.session['idStatus'] if 'idStatus' in request.session else None
#         idTipo=request.session['idTipo'] if 'idTipo' in request.session else None
#         idOrigen=request.session['idOrigen'] if 'idOrigen' in request.session else None
#         idSponsor=request.session['idSponsor'] if 'idSponsor' in request.session else None


        

        
#         is_cookie_set = 1

   

#     if request.method == "GET":
      

#       if request.GET.get('page')==None:
#         is_cookie_set = 0
#         request.session['fechaInicial']=None
#         request.session['fechaFinal']=None
#         request.session['idPersona']=None
#         request.session['idStatus']=None
#         request.session['idOrigen']=None

#         request.session['idTipo']=None
        
#         request.session['idSponsor']=None
#         fechaF=None
#         fechaI=None
#         idPersona=None
#         idStatus=None
#         idTipo=None
#         idOrigen=None
#         idSponsor=None
      
      
#       if (is_cookie_set == 1): 
#           if fechaI!=None and fechaI!="":

#            dateI=parse_datetime(fechaI+' 00:00:00-00')
           
         
#            matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE pmat.fecha_matricula =%s"%(f4_str))
#           if fechaF!=None  and fechaF!="":

#            dateF=parse_datetime(fechaF+' 00:00:00-00')
          
          
#            matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE pmat.fecha_matricula =%s"%(f3_str))
#            print
#           if idPersona!=None and idPersona!="":
#            matriculaList=matriculaList.filter(fk_publico=idPersona)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE app.fk_publico_id =%s"%(idPersona))
#           if idTipo!=None and idTipo!="":
#            matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.fk_tipo_matricula_id =%s"%(idTipo))
#           if idStatus!=None and idStatus!="":
#            matriculaList=matriculaList.filter(fk_status_matricula=idStatus)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.fk_status_matricula_id =%s"%(idStatus))
#           if idOrigen!=None and idOrigen!="":
#            matriculaList=matriculaList.filter(origenSolicitud=idOrigen)
#            #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.origenSolicitud =%s"%(idOrigen))
#           if idSponsor!=None and idSponsor!="":
#            matriculaList=matriculaList.filter(fk_publico__extensionusuario__CtaUsuario__sponsor_code_id=idSponsor)
           
           


           




#     if request.method == "POST":
        
#         if (is_cookie_set == 1): 
          
#           request.session['fechaInicial']=None
#           request.session['fechaFinal']=None
#           request.session['idPersona']=None
#           request.session['idStatus']=None
#           request.session['idTipo']=None
#           request.session['idOrigen']=None
#           request.session['idSponsor']=None


       

#         fechaInicial=request.POST.get('fechaInicial') 
        

#         print(request.POST)
       
#         fechaFinal=request.POST.get('fechaFinal') 
#         idPersona=request.POST.get('PersonId') 
#         idStatus=request.POST.get('idStatus') 
#         idTipo=request.POST.get('idTipo') 
#         idOrigen=request.POST.get('idOrigen') 
#         idSponsor=request.POST.get('idSponsor') 

        
     
#         if idTipo!= None and idTipo!="":
#          matriculaList=matriculaList.filter(fk_tipo_matricula=idTipo)
#          #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.fk_tipo_matricula_id =%s"%(idTipo))
#          request.session['idTipo'] = idTipo
#         if idOrigen!= None and idOrigen!="":
#          matriculaList=matriculaList.filter(origenSolicitud=idOrigen)
#          #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.origenSolicitud =%s"%(idOrigen))

#          request.session['idOrigen'] = idOrigen

#         print("request.POST")

#         if idStatus != None and idStatus!="":
#          print("eke")
         
#          matriculaList=matriculaList.filter(fk_status_matricula=idStatus)
#          #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE  pmat.fk_status_matricula_id =%s"%(idStatus))
#          request.session['idStatus'] = idStatus
#         if idPersona != None and idPersona!="" :
         
#          print(idPersona)
#          #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE app.fk_publico_id =%s"%(idPersona))
#          matriculaList=matriculaList.filter(fk_publico=idPersona)
#          request.session['idPersona'] = idPersona

        
#         if fechaInicial != None and fechaInicial!="":
#           dateI=parse_datetime(fechaInicial+' 00:00:00-00')
#           fechaI=fechaInicial
         
          
         
#           request.session['fechaInicial'] = fechaI
         
         
          
#           matriculaList=matriculaList.filter(fecha_matricula__gte=dateI)
#           #matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE pmat.fecha_matricula = %s " %f1_str)
#           print(matriculaList)
#         if fechaFinal != None and fechaFinal!="":
#           dateF=parse_datetime(fechaFinal+' 00:00:00-00')
          
#           request.session['fechaFinal'] = fechaF
         
#           matriculaList=matriculaList.filter(fecha_matricula__lte=dateF)
#           #matriculaList=matriculaList=MatriculaAlumnos.objects.raw("SELECT * FROM app_publico AS appu JOIN registration_matriculaalumnos AS pmat ON pmat.fk_publico_id=appu.idpublico JOIN registration_matriculaspagos AS pag ON pag.fk_matricula_alumnos_id=pmat.idmatricula_alumnos JOIN security_extensionusuario AS exts ON exts.publico_id=appu.idpublico JOIN security_ctausuario AS cta ON cta.idcta_usuario=exts.ctausuario_id WHERE pmat.fecha_matricula = %s" %f2_str)
#         if idSponsor!=None and idSponsor!="":
#           request.session['idSponsor'] = idSponsor
#           matriculaList=matriculaList.filter(fk_publico__extensionusuario__CtaUsuario__sponsor_code_id=idSponsor)
           
          

        
          




    
#     paginator = Paginator(matriculaList, 10)
#     origenes=Methods.getOrigenesMatricula()
    
    
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     if idPersona!=None and idPersona!="" :
#      personaBuscarNombre=Publico.objects.get(pk=idPersona)
#     else:
#       personaBuscarNombre=""
#       idPersona=""
    
#     if idStatus!=None and idStatus!="":
#      idStatus=int(idStatus)
#     if idTipo!=None and idTipo!="":
#      idTipo=int(idTipo)
#     if idOrigen!=None and idOrigen!="":
#      idOrigen=int(idOrigen)
#     if idSponsor!=None and idSponsor!="":
#      idSponsor=int(idSponsor)
            
#     #context = { 'msg':msg,'matriculasList': matriculaList}
#     #context['segment'] = 'registration'
    

    
#     html_template = (loader.get_template('registration/matriculasadminstrar.html'))

#     context={'msg':msg,
#     'matriculasList': page_obj,
#     'FechaInicial':fechaI,
#     'FechaFinal':fechaF,
     
#      'idPersona':idPersona,
#      'personaBuscarNombre':personaBuscarNombre,
#       'selectedStatus':idStatus,
#       'selectedType':idTipo ,
#       'status':status,'types':types,
#       'sponsor':sponsor,
#        'segment':'registration',
#         'origenes':origenes,
#         'idOrigen':idOrigen} 
    
    
#    # return HttpResponse(html_template.render(context, request))
#     return render(request, 'registration/matriculasadminstrar.html', context)
# def comboboxpro(request):
    
#     valor=request.GET.get('valor')
#     tipo=request.GET.get('tipo')
#     hay=False
#     print(valor)
#     print(tipo)
#     if tipo == "componente":
#         hay=1
#     elif tipo == "atv":
#         hay=2    
#     data = {'opsion2': metodo_llenar_combo(valor,tipo),'hay':hay}
#     print(data)
#     html_template = (loader.get_template('comboboxpro.html'))
#     return HttpResponse(html_template.render(data, request)) 
# def metodo_llenar_combo(valor,tipo):
#     valor1=valor
#     tipo2=tipo
#     if tipo2 == "pro":
#        result1=Estructuraprograma.objects.filter(fk_estructura_padre_id=valor1,valor_elemento="Process")
#        print(result1)
#        lista=[]

#        for file in result1:
        
#            lista.append(file)
#        print(lista)    
#        return lista                     
    
    
    
                  