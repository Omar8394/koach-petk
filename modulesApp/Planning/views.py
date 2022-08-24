from distutils.log import error
from django.http import HttpResponse, JsonResponse
from django.template import loader
import time, json
from .models import fichas, fichas_bloques, atributosxfichaxbloque
from ..App.models import ConfTablasConfiguracion as configuraciones

# Create your views here.

def func_Planning(request): 
    context = {}
    html_template = loader.get_template( 'TabPersonal/carpPlanning/crear_ficha.html' )
    return HttpResponse(html_template.render(context, request))

def render_fihas(request): 
    context = {}
    ficha = fichas.objects.all()
    context['data'] = ficha
    html_template = loader.get_template( 'TabPersonal/renderfihas.html' )
    return HttpResponse(html_template.render(context, request))

def testfi(request): 
    context = {}

    html_template = loader.get_template( 'TabPersonal/carpPlanning/testfi.html' )
    return HttpResponse(html_template.render(context, request))

def modalFicha(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            id = int(body.get('id'))

            try:

                ficha = fichas.objects.get(id_ficha=id)
                context['data'] = ficha

            except:
                
                pass

    html_template = loader.get_template( 'TabPersonal/carpPlanning/modalFicha.html' )
    return HttpResponse(html_template.render(context, request))

def validarNombreFicha(request): 

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            nombre = body.get('nombre')
            id = int(body.get('id'))
            ficha = fichas.objects.filter(nombre_ficha=nombre).exclude(id_ficha=id)

            if not ficha:
                
                return JsonResponse({'valido':'valido'})

    return HttpResponse()

    
def guardarFicha(request): 

    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            data = body.get('data')
            id = body.get('id')

            if data:

                if id and int(id) > 0:

                    ficha = fichas.objects.get(id_ficha=id)

                else: 

                    ficha = fichas()

                ficha.nombre_ficha = data.get('nombre')
                ficha.mostrar = 1
                if not int(id) > 0:
                    ficha.ordenamiento = len(fichas.objects.all()) + 1
                ficha.save()

    context['data'] = fichas.objects.all()
    html_template = loader.get_template( 'TabPersonal/renderfihas.html' )
    return HttpResponse(html_template.render(context, request))

    
def eliminarFicha(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            id = int(body.get('id'))
            ficha = fichas.objects.get(id_ficha=id)
            ficha.delete()

    context['data'] = fichas.objects.all()
    html_template = loader.get_template( 'TabPersonal/renderfihas.html' )
    return HttpResponse(html_template.render(context, request))

    
def moverFicha(request): 

    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            data = body.get('data')
            Fichas = fichas.objects.all()

            i = 1
            for d in data:

                ficha = Fichas.get(id_ficha=d)
                ficha.ordenamiento = i
                i = i + 1
                ficha.save()
            
        Fichas = fichas.objects.all()
        context['data'] = Fichas
    html_template = (loader.get_template('TabPersonal/renderfihas.html'))
    return HttpResponse(html_template.render(context, request))

def modalListaBloque(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            id = int(body.get('id'))

            try:

                ficha = fichas.objects.get(id_ficha=id)
                context['ficha'] = ficha
                bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id)
                context['data'] = bloques

            except:
                
                pass
            
    html_template = loader.get_template( 'TabPersonal/carpPlanning/modalListaBloque.html' )
    return HttpResponse(html_template.render(context, request))

    
def modalBloque(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            idBloque = int(body.get('idBloque'))

            try:

                bloque = fichas_bloques.objects.get(id_bloquexficha=idBloque)
                context['data'] = bloque

            except:
                
                pass

    html_template = loader.get_template( 'TabPersonal/carpPlanning/modalBloque.html' )
    return HttpResponse(html_template.render(context, request))
    
def guardarBloque(request): 

    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            data = body.get('data')
            id = body.get('id')
            idBloque = body.get('idBloque')

            if data:

                if idBloque and int(idBloque) > 0:

                    bloque = fichas_bloques.objects.get(id_bloquexficha=idBloque)

                else: 

                    bloque = fichas_bloques()

                bloque.descrip_bloque = data.get('descripcion')
                ficha = fichas.objects.get(id_ficha=id)
                bloque.fk_idficha = ficha
                if not int(idBloque) > 0:
                    bloque.ordenamiento = len(fichas_bloques.objects.filter(fk_idficha=ficha)) + 1
                bloque.save()

    
    ficha = fichas.objects.get(id_ficha=id)
    context['ficha'] = ficha
    bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id)
    context['data'] = bloques
    html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoListaBloque.html' )
    return HttpResponse(html_template.render(context, request))

def eliminarBloque(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            id = body.get('id')
            idBloque = int(body.get('idBloque'))
            bloque = fichas_bloques.objects.get(id_bloquexficha=idBloque)
            bloque.delete()

    ficha = fichas.objects.get(id_ficha=id)
    context['ficha'] = ficha
    bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id)
    context['data'] = bloques
    html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoListaBloque.html' )
    return HttpResponse(html_template.render(context, request))

    
def moverBloque(request): 

    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            id = body.get('id')
            data = body.get('data')
            bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id)

            if bloques:

                i = 1
                for d in data:

                    bloque = bloques.get(id_bloquexficha=d)
                    bloque.ordenamiento = i
                    i = i + 1
                    bloque.save()
                
            bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id) 
            context['data'] = bloques
            ficha = fichas.objects.get(id_ficha=id)
            context['ficha'] = ficha

    html_template = (loader.get_template('TabPersonal/carpPlanning/contenidoListaBloque.html'))
    return HttpResponse(html_template.render(context, request))

    
def modalAtributo(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            idBloque = int(body.get('idBloque'))
            
            try:

                bloque = fichas_bloques.objects.get(id_bloquexficha=idBloque)
                context['bloque'] = bloque
                lista = configuraciones.obtenerHijos('Tipo_Atributo')
                context['lista'] = lista
                context['data'] = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=idBloque)
                # bloques = fichas_bloques.objects.filter(fk_idficha__id_ficha=id)
                # context['data'] = bloques

            except:

                pass
            
    html_template = loader.get_template( 'TabPersonal/carpPlanning/modalAtributos.html' )
    return HttpResponse(html_template.render(context, request))

def guardarAtributo(request): 

    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            data = body.get('data')
            idBloque = body.get('idBloque')
            idAtributo = body.get('idAtributo')


            if idAtributo and int(idAtributo) > 0:

                atributo = atributosxfichaxbloque.objects.get(id_atribxfichaxbloq=idAtributo)

            else: 

                atributo = atributosxfichaxbloque()

            if data:

                atributo.nombre_atrib = data.get('nombre') 
                atributo.fk_tipodato = data.get('nombre') 

            if not idAtributo:

                atributo.orden_presentacion = len(atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=idBloque)) + 1

            bloque = fichas_bloques.objects.get(id_bloquexficha=idBloque)
            atributo.fk_ficha_bloque = bloque
            atributo.save()
            context['page'] = atributo
            lista = configuraciones.obtenerHijos('Tipo_Atributo')
            context['lista'] = lista

    html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoAtributoIndividual.html' )
    return HttpResponse(html_template.render(context, request))

    
def eliminarAtributo(request): 
    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            idAtributo = body.get('idAtributo')
            atributo = atributosxfichaxbloque.objects.get(id_atribxfichaxbloq=idAtributo)
            atributo.delete()

    return HttpResponse('ok')
    
def moverAtributo(request): 

    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            id = body.get('id')
            data = body.get('data')
            atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=id)

            if atributos:

                i = 1
                for d in data:

                    atributo = atributos.get(id_atribxfichaxbloq=d)
                    atributo.orden_presentacion = i
                    i = i + 1
                    atributo.save()
                
            context['data'] = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=id)
            lista = configuraciones.obtenerHijos('Tipo_Atributo')
            context['lista'] = lista

    html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoAtributo.html' )
    return HttpResponse(html_template.render(context, request))

       
def atributoLista(request): 

    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            value = body.get('value')
            lista = configuraciones.objects.get(id_tabla=value)

            if lista.valor_elemento == 'Tipo_Atributo_Rango' or lista.valor_elemento == 'Tipo_Atributo_Texto' or lista.valor_elemento == 'Tipo_Atributo_Texto_Largo' or lista.valor_elemento == 'Tipo_Atributo_Fecha':

                return HttpResponse()

            elif lista.valor_elemento == 'Tipo_Atributo_Seleccion' or lista.valor_elemento == 'Tipo_Atributo_Lista' or lista.valor_elemento == 'Tipo_Atributo_Seleccion_Multiple':

                context['lista'] = lista
                html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoListaAtributo.html' )
                return HttpResponse(html_template.render(context, request))

    return HttpResponse()