from django import template
from django.db.models.aggregates import Count
from datetime import date
import datetime
import random
from django.utils import timezone
import json
from datetime import timedelta
from django.core import serializers
from django.db.models import Q
from modulesApp.Security.models import User
from modulesApp.App.models import ConfTablasConfiguracion,AppPublico
from modulesApp.Capacitacion.models import Estructuraprograma, capacitacion_ActSesiones_programar, capacitacion_Actividad_Sesiones, capacitacion_Actividad_leccion, capacitacion_Actividad_tareas, capacitacion_ComponentesActividades, capacitacion_EvaluacionesPreguntas, capacitacion_EvaluacionesPreguntasOpciones, capacitacion_LeccionPaginas, capacitacion_Recursos,capacitacion_componentesXestructura,componentesFormacion,capacitacion_Tag,capacitacion_TagRecurso,capacitacion_componentesPrerequisitos,EscalasEvaluaciones,capacitacion_ActividadEvaluaciones,capacitacion_EvaluacionesBloques,capacitacion_ActividadesTiempoReal,capacitacion_Examenes,capacitacion_HistoricoActividades  
from modulesApp.Organizational_network.models import nodos_gruposIntegrantes,nodos_PlanFormacion
from modulesApp.App.models import ConfSettings,ConfSettings_Atributo
register = template.Library()

@register.filter(name='week')
def week(topico, usuario):
    
    rol=usuario.fk_rol_usuario
    userpu= AppPublico.objects.get(user_id=usuario)
    rango=ConfSettings_Atributo.objects.get(valor_setting='avance_temas')   
    datos=json.loads(rango.rangovalor_setting)
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)   
    _isFree = False
    if str(rol) == 'Estudiante':
      if rango.status_setting == 1:
        
        date =datetime.datetime.now()
        start_week = date - datetime.timedelta(date.weekday())
        sem=datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)
        mydate = end_week - timedelta(days=6)
        mydate = mydate.replace(hour=00,minute=00,second=00, microsecond=00000)       
        lastTopics = capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=nodosuser, fecha_realizado__gte=mydate).values('fk_componenteActividades__fk_componenteformacion').annotate(lecciones=Count('fk_componenteActividades')) 
        
        if lastTopics.exists():
            
            if lastTopics.count() >= int(datos['max']) : 
               print('hui')            
               for topic in lastTopics:      
                  if topico.pk == topic['fk_componenteActividades__fk_componenteformacion'] :    
                     print('asi')
                     print(topic['fk_componenteActividades__fk_componenteformacion'] )
                     return True 
                  
                 # codigo para excepciones  
               olderTopics = capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=nodosuser, fecha_realizado__lte=mydate, fk_componenteActividades__fk_componenteformacion_id=topico.fk_componetesformacion)
               
               if olderTopics.exists():
                  _isFree = True
                  for lesson in olderTopics:
                      if lesson.culminado == 0:
                            return False
               
        #         
               
            else:
               if weekend(topico.fk_componetesformacion, usuario):
                 _isFree=True 
               else:  
                 _isFree=False
                
        else:
           historial=capacitacion_HistoricoActividades.objects.filter(fk_componenteXestructura=topico)
           if historial.exists():
              tema=jsons(historial[0].datos_resumen)
              if topico.fk_componetesformacion_id == int(tema):
                 _isFree=True 
             
           else:
            if weekend(topico.fk_componetesformacion, usuario):
              _isFree=True 
            else:  
              _isFree=False 
      else: 
       _isFree = True          
    else:
        _isFree = True
    return _isFree
@register.filter(name='locked')
def isNeeded(activity, usuario):
    isRequired = False
    rol=usuario.fk_rol_usuario
    userpu= AppPublico.objects.get(user_id=usuario)
   
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
    if str(rol) == 'Estudiante':
        requisitos = capacitacion_componentesPrerequisitos.objects.filter( fk_componenteActividades=activity)
        if requisitos.exists():
            for requisito in requisitos:
                visto = capacitacion_ActividadesTiempoReal.objects.filter(fk_nodo_Grupo_integrantes=nodosuser, fk_componenteActividades=requisito.fk_prerequisito, culminado=True)
                if not visto.exists():
                    isRequired=True
                    break
    return isRequired
@register.filter(name='weekend')
def weekend(topico, usuario):
    print('koal')
    print(topico)
    rol=usuario.fk_rol_usuario
    userpu= AppPublico.objects.get(user_id=usuario)    
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
    grupo=nodosuser.fk_nodogrupo
    rango=ConfSettings_Atributo.objects.get(valor_setting='avance_temas') 
    print(rango)  
    datos=json.loads(rango.rangovalor_setting)
    date =datetime.datetime.now()
    start_week = date - datetime.timedelta(date.weekday())
    em=datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(6)
    mydate = end_week - timedelta(days=6)
    mydate = mydate.replace(hour=00,minute=00,second=00, microsecond=00000)
    
    _isFree = False
    if str(rol) == 'Estudiante':
       semanatest=capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes=nodosuser,fecha_final__gte=mydate) 
       
       print(datos['max'])
       if semanatest.exists():
          if semanatest.count() >= int(datos['max']):
            _isFree = False
          else:
              orden_anterior = topico.orden_presentacion - 1 
       
              topico_anterior = nodos_PlanFormacion.objects.filter(fk_gruponodo=grupo, orden_presentacion=orden_anterior)
      
              if topico_anterior.exists():
                 lista_examenes=capacitacion_ActividadEvaluaciones.objects.filter(fk_componenteActividad__fk_componenteformacion=topico_anterior[0].fk_componentesXestructura.fk_componetesformacion) 
                 print('huuyi')
                 if lista_examenes.exists():
                    print('no')        
                    for test in lista_examenes:
                
                        actividad = test.id_ActividadEvaluaciones
                 
                        test_aprobados = capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes_id=nodosuser.pk,fk_ActividadEvaluaciones_id=actividad,puntuacion_obtenida__gte=test.calificacion_aprobar)
                        print(test_aprobados)
                        if test_aprobados.exists():
                           _isFree=True
                        else:
                    
                           return False
                 else:
                   _isFree = False  
              else:
                _isFree = True          
    
       else:    
          orden_anterior = topico.orden_presentacion - 1 
       
          topico_anterior = nodos_PlanFormacion.objects.filter(fk_gruponodo=grupo, orden_presentacion=orden_anterior)
      
          if topico_anterior.exists():
             lista_examenes=capacitacion_ActividadEvaluaciones.objects.filter(fk_componenteActividad__fk_componenteformacion=topico_anterior[0].fk_componentesXestructura.fk_componetesformacion) 
             print('huuyi')
             if lista_examenes.exists():
                print('no')        
                for test in lista_examenes:
                
                    actividad = test.id_ActividadEvaluaciones
                 
                    test_aprobados = capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes_id=nodosuser.pk,fk_ActividadEvaluaciones_id=actividad,puntuacion_obtenida__gte=test.calificacion_aprobar)
                    print(test_aprobados)
                    if test_aprobados.exists():
                       _isFree=True
                    else:
                    
                       return False
             else:
               _isFree = False  
          else:
             _isFree = True          
       print(_isFree)      
    return _isFree   
@register.filter(name='nextActivity')
def nextActivity(activity, tems):
    print(tems)  
    tem=''
         
    componente=capacitacion_ComponentesActividades.objects.get(pk=activity,fk_componenteformacion=tems)
    print(componente)
    nextPosicion=componente.orden_presentacion + 1
    nextActivity = capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=tems, orden_presentacion=nextPosicion)
    print(nextActivity)
    if nextActivity.exists():
        tem=nextActivity[0]
           
    else:
      temass= componentesFormacion.objects.filter(pk=tems.pk)
      print(temass)
      if temass.exists():
         tem_orden=temass[0].orden_presentacion + 1
         temasA=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion__orden_presentacion=tem_orden)
         print(tem_orden)
         if temasA.exists(): 
            tem= temasA[0] 
           
      
    print(tem)   
    return tem  
@register.filter(name='previousActivity')
def previousActivity(activity, user):
    temas=capacitacion_ComponentesActividades.objects.get(pk=activity)
    print(temas)
    nextPosicion=temas.orden_presentacion - 1
    prevActivity = capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=temas.fk_componenteformacion, orden_presentacion=nextPosicion)
    if prevActivity.exists():
        if isNeeded(prevActivity[0],user):
            return None
    else:
            return None
    return prevActivity[0]
def jsons(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'datos_resumen' in data :
     return data['datos_resumen'][0]['tema']
  else:
      return ""

  