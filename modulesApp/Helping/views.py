import imghdr
from django.shortcuts import render
from .forms import helpingImageForm
from .models import tutoriales, paginas as paginasHelping, helpingImage
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import HttpResponse
import json



def nuevo(request): 

    return render(request,"Helping/ayuda.html", {}) 
   

   
def modalAddPagina(request): 

    context = {}

    if(request.body):

        
        body = json.load(request)
        fk = body['fk']
        id = body['id']

        helping=tutoriales.objects.get(idtutorial=fk)
        context = {'data': helping}

        if int(id) > 0:

            paginas=paginasHelping.objects.get(idpagina=id)
            context = {'data': helping, 'pagina' : paginas}
 
    html_template = (loader.get_template('Helping/modalPagina.html'))
    return HttpResponse(html_template.render(context, request))

    
def modalGuardarPagina(request): 

    if request.body:

        body = json.load(request)
        data = body['data']
        id = body['id']
        fk = body['fk']

        
        helping=tutoriales.objects.get(idtutorial=fk)

        if int(id) > 0:

            pagina=paginasHelping.objects.get(idpagina=id)

        else: 
            pagina = paginasHelping()

        pagina.fk_tutorial=helping
        pagina.contenido=data['descripcion']
        pagina.url=""
        pagina.save()

    html_template = (loader.get_template('Helping/modalPagina.html'))
    return HttpResponse(html_template.render({}, request))

def modalHijosPagina(request): 

    context = {}

    if(request.body):

        id = json.load(request)['id']
        helping=tutoriales.objects.get(idtutorial=id)

        if helping:

            paginas=paginasHelping.objects.filter(fk_tutorial__idtutorial=id)
            context = {'data': helping, 'paginas':paginas}
 
    html_template = (loader.get_template('Helping/modalHijosPagina.html'))
    return HttpResponse(html_template.render(context, request))

def modalAddCarruserl(request): 

    context = {}

    if(request.body):

        id = json.load(request)['id']
        helping=tutoriales.objects.get(idtutorial=id)

        if helping:

            paginas=paginasHelping.objects.filter(fk_tutorial__idtutorial=id)
            context = {'data': helping, 'paginas':paginas}

            if not paginas: 
                return HttpResponse()
    html_template = (loader.get_template('Helping/modalCarrusel.html'))
    return HttpResponse(html_template.render(context, request))

def modalAddAyuda(request): 

    context = {}

    if(request.body):

        id = json.load(request)['id']

        if int(id) > 0:

            helping=tutoriales.objects.get(idtutorial=id)
            context = {'data': helping}
 
    html_template = (loader.get_template('Helping/modalAyuda.html'))
    return HttpResponse(html_template.render(context, request))

def modalGuardarAyuda(request): 

    if request.body:

        body = json.load(request)
        data = body['data']
        id = body['id']

        if id and int(id) > 0:

            helping=tutoriales.objects.get(idtutorial=id)

        else: 
            helping = tutoriales()

        helping.titulo=data['titulo']
        helping.descripcion=data['descripcion']
        helping.url=""
        helping.tipo= int(data.get('tipo', 1))
        helping.ordenamiento = 0

        helping.save()

    helping = tutoriales.objects.all()
    html_template = (loader.get_template('Helping/contenidoAyuda.html'))
    return HttpResponse(html_template.render({'data': helping}, request))
    
def modalGuardarImagen(request): 


    form = helpingImageForm(request.POST, request.FILES)
    imagen = None

    if form.is_valid():

        imagen = form.save()

    html_template = (loader.get_template('Helping/image.html'))
    return HttpResponse(html_template.render({'data': imagen}, request))

def modalEliminarImagen(request): 

    if request.body:

        url = str(json.load(request)['file']).replace('/media/','')
        
        try:

            img_help = helpingImage.objects.get(imagen = url)

        except:

            img_help = None

        if img_help:

            img_help.imagen.delete(save=True)
            img_help.delete()

    return JsonResponse({})

def modalEliminarAyuda(request): 

    if request.body:

        id = json.load(request)['id']
        helping=tutoriales.objects.get(idtutorial=id)
        helping.delete()
    # img_help =helpingImage.objects.get(id=33)
    # img_help.url.delete(save=True)
    # img_help.delete()
    helping = tutoriales.objects.all()
    html_template = (loader.get_template('Helping/contenidoAyuda.html'))
    return HttpResponse(html_template.render({'data': helping}, request))


def modalEliminarHijoPagina(request): 

    if request.body:

        body = json.load(request)
        id = body['id']
        fk = body['fk']
        
        paginas=paginasHelping.objects.get(idpagina=id)
        paginas.delete()

    helping=tutoriales.objects.get(idtutorial=fk)
    paginas=paginasHelping.objects.filter(fk_tutorial__idtutorial=fk)
    html_template = (loader.get_template('Helping/modalHijosPagina.html'))
    return HttpResponse(html_template.render({'data': helping, 'paginas':paginas}, request))