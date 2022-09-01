from distutils.log import error
from django.http import HttpResponse, JsonResponse
from django.template import loader
import time, json, re
from .models import fichas, fichas_bloques, atributosxfichaxbloque, public_fichas_datos
from ..App.models import AppPublico, ConfTablasConfiguracion as configuraciones
from django.template.defaulttags import register
from django.shortcuts import render

# Create your views here.

@register.filter
def tosJson(value):

    lista = json.loads(value)
    lista = {k: v for k, v in lista.items() if v}
    return lista.items()

def func_Planning(request): 

    context = {}
    html_template = loader.get_template( 'TabPersonal/carpPlanning/crear_ficha.html' )
    return HttpResponse(html_template.render(context, request))

def render_fihas(request): 
    
    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            tipo = body.get('tipo')

            if tipo:

                context['tipo'] = tipo
                ficha = fichas.objects.all()
                res = fichas.objects.all()

                for f in ficha:

                    bloques = fichas_bloques.objects.filter(fk_idficha=f)
                    atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__fk_idficha=f)

                    if bloques and atributos:

                        borrar = True

                        for atributo in atributos:

                            if atributo.nombre_atrib and str(atributo.nombre_atrib).strip() and atributo.fk_tipodato:

                                if atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Seleccion' or atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Lista' or atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Seleccion_Multiple':

                                    if atributo.listaValores:

                                        lista = json.loads(atributo.listaValores)
                                        lista = {k: v for k, v in lista.items() if v}

                                        if lista:
                                            
                                            borrar = False
                                            break

                                else:
                                    
                                    borrar = False
                                    break

                        if borrar:

                            res = res.exclude(id_ficha=f.id_ficha)


                    else:

                        res = res.exclude(id_ficha=f.id_ficha)

                context['data'] = res
                html_template = loader.get_template( 'TabPersonal/renderfihas.html' )
                return HttpResponse(html_template.render(context, request))

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

def previsualizarFicha(request, idFicha): 

    try:

        context = {}
        ficha = fichas.objects.get(id_ficha=idFicha)
        context['ficha'] = ficha
        bloque = fichas_bloques.objects.filter(fk_idficha=ficha)
        context['bloques'] = bloque
        atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__fk_idficha=ficha)
        context['atributos'] = atributos
        html_template = loader.get_template('TabPersonal/carpPlanning/previsualizarFicha.html')
        return HttpResponse(html_template.render(context, request))

    except:

        return render(request, "Helping/404error.html", {})

    
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

def previsualizarBloque(request, idFicha, id): 

    try:

        context = {}
        ficha = fichas.objects.get(id_ficha=idFicha)
        context['ficha'] = ficha
        bloque = fichas_bloques.objects.get(id_bloquexficha=id)
        context['bloque'] = bloque
        atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque=bloque)
        context['atributos'] = atributos
        html_template = loader.get_template( 'TabPersonal/carpPlanning/previsualizarBloque.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        return render(request, "Helping/404error.html", {})

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
                atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=idBloque)
                context['data'] = atributos

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


            if data:

                guardarAtributos(idBloque, data)
                return HttpResponse('ok')
            
            else:

                if idAtributo and int(idAtributo) > 0:

                    atributo = atributosxfichaxbloque.objects.get(id_atribxfichaxbloq=idAtributo)

                else: 

                    atributo = atributosxfichaxbloque()


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

def guardarAtributos(idBloque, data):

    if data:

        atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=idBloque)

        for atributo in atributos:

            atributo.listaValores = None
            atributo.save()

        for x, y in data.items():
            # if(y):
                # print(x)
                try:

                    id = re.search("[0-9]+", x).group()
                    tipo = re.search("[a-zA-Z]*", x).group()
                    atributo = atributos.get(id_atribxfichaxbloq=id)

                    if tipo == 'Tipo':

                        lista = configuraciones.obtenerHijos('Tipo_Atributo')
                        tipoAtributo = lista.get(id_tabla=y)

                        if tipoAtributo:

                            atributo.fk_tipodato = tipoAtributo

                            if tipoAtributo.valor_elemento == 'Tipo_Atributo_Rango' or tipoAtributo.valor_elemento == 'Tipo_Atributo_Texto' or tipoAtributo.valor_elemento == 'Tipo_Atributo_Texto_Largo' or tipoAtributo.valor_elemento == 'Tipo_Atributo_Fecha':
                            
                                atributo.listaValores = None
                                atributo.rangos = None
                        
                        else:

                            atributo.listaValores = None
                            atributo.rangos = None

                    elif tipo == 'titulo':

                        atributo.nombre_atrib = y

                    elif tipo == 'lista':

                        jsonList = json.loads(atributo.listaValores) if atributo.listaValores else {}
                        jsonList.update({y: y})
                        atributo.listaValores = json.dumps(jsonList)

                    atributo.save()

                except: 

                    print('error')
    
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
            dataForm = body.get('dataForm')
            atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__id_bloquexficha=id)
            guardarAtributos(id, dataForm)

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
            padre = body.get('padre')
            lista = configuraciones.objects.get(id_tabla=value)

            if lista.valor_elemento == 'Tipo_Atributo_Rango' or lista.valor_elemento == 'Tipo_Atributo_Texto' or lista.valor_elemento == 'Tipo_Atributo_Texto_Largo' or lista.valor_elemento == 'Tipo_Atributo_Fecha':

                return HttpResponse()

            elif lista.valor_elemento == 'Tipo_Atributo_Seleccion' or lista.valor_elemento == 'Tipo_Atributo_Lista' or lista.valor_elemento == 'Tipo_Atributo_Seleccion_Multiple':

                context['lista'] = lista
                context['padre'] = atributosxfichaxbloque.objects.get(id_atribxfichaxbloq=padre).id_atribxfichaxbloq
                html_template = loader.get_template( 'TabPersonal/carpPlanning/contenidoListaAtributo.html' )
                return HttpResponse(html_template.render(context, request))

    return HttpResponse()

def mostrarFicha(request): 
    
    context = {}

    try:

        publico = AppPublico.objects.get(user_id=request.user)

    except:

        context['error'] = 'error'

    html_template = loader.get_template( 'TabPersonal/carpPlanning/mostrarFichas.html' )
    return HttpResponse(html_template.render(context, request))    

def fichaPersonal(request, idFicha): 

    try:

        publico = AppPublico.objects.get(user_id=request.user)

    except:

        return render(request, "Helping/404error.html", {})
    
    try:

        context = {}
        ficha = fichas.objects.get(id_ficha=idFicha)
        bloques = fichas_bloques.objects.filter(fk_idficha=ficha)
        atributos = atributosxfichaxbloque.objects.filter(fk_ficha_bloque__fk_idficha=ficha)

        for bloque in bloques:

            atributo = atributos.filter(fk_ficha_bloque=bloque)

            if not atributo:

                bloques = bloques.exclude(id_bloquexficha=bloque.id_bloquexficha)

        for atributo in atributos:

            if atributo.nombre_atrib and str(atributo.nombre_atrib).strip() and atributo.fk_tipodato:

                if atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Seleccion' or atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Lista' or atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Seleccion_Multiple':

                    if atributo.listaValores:

                        lista = json.loads(atributo.listaValores)
                        lista = {k: v for k, v in lista.items() if v}

                        if not lista:

                            atributos = atributos.exclude(id_atribxfichaxbloq=atributo.id_atribxfichaxbloq)

                    else:

                        atributos = atributos.exclude(id_atribxfichaxbloq=atributo.id_atribxfichaxbloq)

            else:

                atributos = atributos.exclude(id_atribxfichaxbloq=atributo.id_atribxfichaxbloq)

        context['ficha'] = ficha
        context['bloques'] = bloques
        context['atributos'] = atributos
        html_template = loader.get_template('TabPersonal/carpPlanning/fichaPersonal.html')
        return HttpResponse(html_template.render(context, request))

    except:

        return render(request, "Helping/404error.html", {})

def guardarFichaPersonal(request): 

    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            data = body.get('data')
            publico = AppPublico.objects.get(user_id=request.user)

            if data:

                primeros = []

                for x, y in data.items():

                    if y:


                        id = re.search("[0-9]+", x).group()
                        atributo = atributosxfichaxbloque.objects.get(id_atribxfichaxbloq=id)
                            
                        try:
                        
                            guardar = public_fichas_datos.objects.get(id_public=publico, id_atributo_fichaBloque=atributo)

                        except:
                            
                            guardar = public_fichas_datos()

                        guardar.id_public = publico
                        guardar.id_atributo_fichaBloque = atributo

                        if atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Seleccion_Multiple' or atributo.fk_tipodato.valor_elemento == 'Tipo_Atributo_Rango':

                            if not id in primeros:

                                guardar.valor = json.dumps({y:y})
                                primeros.append(id)

                            else:

                                temp = json.loads(guardar.valor)
                                temp.update({y: y})
                                guardar.valor = json.dumps(temp)

                        else:

                            guardar.valor = y

                        guardar.save()

                return HttpResponse('ok')
            
    return HttpResponse('ok')