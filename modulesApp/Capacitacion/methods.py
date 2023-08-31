from ..App.models import ConfTablasConfiguracion,AppPublico
from ..Capacitacion.models import Estructuraprograma, capacitacion_ActSesiones_programar, capacitacion_Actividad_Sesiones, capacitacion_Actividad_leccion, capacitacion_Actividad_tareas, capacitacion_ComponentesActividades, capacitacion_EvaluacionesPreguntas, capacitacion_EvaluacionesPreguntasOpciones, capacitacion_LeccionPaginas, capacitacion_Recursos,capacitacion_componentesXestructura,componentesFormacion,capacitacion_Tag,capacitacion_TagRecurso,capacitacion_componentesPrerequisitos,EscalasEvaluaciones,capacitacion_ActividadEvaluaciones,capacitacion_EvaluacionesBloques,capacitacion_ActividadesTiempoReal,capacitacion_Examenes,capacitacion_ExamenesResultado,capacitacion_NotificacionesMensajesXactividad,capacitacion_HistoricoActividades
from ..Organizational_network.models import nodos_grupos,nodos_gruposIntegrantes,nodos_PlanFormacion
from ..Comunication.models import Comunication_MsjPredeterminado,Boletin_Info 
from modulesApp.App.models import ConfSettings,ConfSettings_Atributo
from django.db.models.aggregates import Count
import time, json
from datetime import date
import datetime
import random
from django.utils import timezone
from datetime import timedelta

def finalizar_componente(usuario,estructura):   
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=usuario)
    print(nodosuser)
    componente=capacitacion_componentesXestructura.objects.get(pk=estructura).fk_componetesformacion
    actividades=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=componente)
    visto=capacitacion_ActividadesTiempoReal.objects.filter(fk_componenteActividades__fk_componenteformacion=componente,culminado=1,fk_nodo_Grupo_integrantes=nodosuser).values('fk_componenteActividades__fk_componenteformacion').annotate(lecciones=Count('fk_componenteActividades'))           
    
    cantidades=actividades.count()
    print(cantidades)
    _isFree = False
    if visto.exists():
       for vistos in visto:
           print(vistos['lecciones'])
           if cantidades == vistos['lecciones']:
              _isFree= True
    print(_isFree)       
    return _isFree  
def verifylast(asti):
    
    tema=asti.fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion
    ultimo=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=tema).order_by('-orden_presentacion')
    print(ultimo)
    if ultimo.exists():
       ultimo[0]
         
    return ultimo[0]   
def week(topico, usuario,ultimo):
   
    rol=usuario.fk_rol_usuario
    userpu= AppPublico.objects.get(user_id=usuario)
    rango=ConfSettings_Atributo.objects.get(valor_setting='avance_temas')   
    datos=json.loads(rango.rangovalor_setting)
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu) 
    date =datetime.datetime.now()
    start_week = date - datetime.timedelta(date.weekday())
    em=datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(6)
    mydate = end_week - timedelta(days=6)
    mydate = mydate.replace(hour=00,minute=00,second=00, microsecond=00000)
      
    _isFree = False
    if str(rol) == 'Estudiante':
      if rango.status_setting == 1:    
         semanatest=capacitacion_Examenes.objects.filter(fk_nodo_Grupo_integrantes=nodosuser,fecha_final__gte=mydate) 
         print(semanatest)
         print(datos['max'])
         if semanatest.exists():
            print('si')    
            if semanatest.count() >= int(datos['max']):
               ultimo_ver=semanatest.order_by('-fk_ActividadEvaluaciones__fk_componenteActividad__fk_componenteformacion__orden_presentacion')    
               print(ultimo_ver[0].fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion.orden_presentacion)
               ultima_ast=capacitacion_ComponentesActividades.objects.filter(fk_componenteformacion=ultimo_ver[0].fk_ActividadEvaluaciones.fk_componenteActividad.fk_componenteformacion).order_by('-orden_presentacion')[0].pk
               if ultimo.pk == ultima_ast:
                   
                  _isFree = False
               else:
                  _isFree = True                
            else: 
             _isFree = True   
         else: 
           _isFree = True       
          
      else: 
       _isFree = True          
    else:
        _isFree = True
    return _isFree


def weekend(topico, usuario):
    print('koal')
    print(topico)
    rol=usuario.fk_rol_usuario
    userpu= AppPublico.objects.get(user_id=usuario)    
    nodosuser=nodos_gruposIntegrantes.objects.get(fk_public=userpu)
    rango=ConfSettings_Atributo.objects.get(valor_setting='avance_temas')   
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
       print(semanatest.count())
       print(datos['max'])
       if semanatest.exists():
          if semanatest.count() >= int(datos['max']):
            _isFree = False
          else:
              orden_anterior = topico.orden_presentacion - 1 
       
              topico_anterior = nodos_PlanFormacion.objects.filter(fk_gruponodo=2, orden_presentacion=orden_anterior)
      
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
       
          topico_anterior = nodos_PlanFormacion.objects.filter(fk_gruponodo=2, orden_presentacion=orden_anterior)
      
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