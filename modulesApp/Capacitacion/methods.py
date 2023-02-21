from ..App.models import ConfTablasConfiguracion,AppPublico
from ..Capacitacion.models import Estructuraprograma, capacitacion_ActSesiones_programar, capacitacion_Actividad_Sesiones, capacitacion_Actividad_leccion, capacitacion_Actividad_tareas, capacitacion_ComponentesActividades, capacitacion_EvaluacionesPreguntas, capacitacion_EvaluacionesPreguntasOpciones, capacitacion_LeccionPaginas, capacitacion_Recursos,capacitacion_componentesXestructura,componentesFormacion,capacitacion_Tag,capacitacion_TagRecurso,capacitacion_componentesPrerequisitos,EscalasEvaluaciones,capacitacion_ActividadEvaluaciones,capacitacion_EvaluacionesBloques,capacitacion_ActividadesTiempoReal,capacitacion_Examenes,capacitacion_ExamenesResultado,capacitacion_NotificacionesMensajesXactividad
from ..Organizational_network.models import nodos_grupos,nodos_gruposIntegrantes,nodos_PlanFormacion
from ..Comunication.models import Comunication_MsjPredeterminado,Boletin_Info 
from django.db.models.aggregates import Count
import time, json

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