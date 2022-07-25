from django.shortcuts import render
from .forms import helpingImageForm, helpingPdfForm
from .models import helpingPdf, tutoriales, paginas as paginasHelping, helpingImage
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import HttpResponse
import json
from django.db.models import Q

def nuevo(request): 

    return render(request,"Helping/ayuda.html", {}) 
   

   
def modalAddPagina(request): 

    context = {}

    if request.method == "POST":

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

    context = {}

    if request.method == "POST":

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
            pagina.titulo=data['titulo']
            pagina.url=""
            if not int(id) > 0:
                pagina.ordenamiento = len(paginasHelping.objects.filter(fk_tutorial=helping)) + 1
            pagina.save()
            borrar_imagenes()
            borrar_pdfs()
            paginas = paginasHelping.objects.filter(fk_tutorial=helping)
            context = {'data': helping, 'paginas':paginas}

    html_template = (loader.get_template('Helping/modalHijosPagina.html'))
    return HttpResponse(html_template.render(context, request))

def modalHijosPagina(request): 

    context = {}

    if request.method == "POST":

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
    
    if request.method == "POST":

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

    if request.method == "POST":

        if(request.body):

            id = json.load(request)['id']

            if int(id) > 0:

                helping=tutoriales.objects.get(idtutorial=id)
                context = {'data': helping}
    
    html_template = (loader.get_template('Helping/modalAyuda.html'))
    return HttpResponse(html_template.render(context, request))

def modalGuardarAyuda(request): 

    if request.method == "POST":

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

    imagen = None

    if request.method == "POST":

        form = helpingImageForm(request.POST, request.FILES)

        if form.is_valid():

            imagen = form.save()
        
        else:

            return HttpResponse()

    html_template = (loader.get_template('Helping/image.html'))
    return HttpResponse(html_template.render({'data': imagen}, request))

def modalGuardarPdf(request): 

    pdf = None

    if request.method == "POST":

        form = helpingPdfForm(request.POST, request.FILES)

        if form.is_valid():

            pdf = form.save()
        
        else:

            return HttpResponse()

    html_template = (loader.get_template('Helping/pdf.html'))
    return HttpResponse(html_template.render({'data': pdf}, request))

def modalEliminarImagen(request): 

    if request.method == "POST":

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

def borrar_imagenes():

    images = helpingImage.objects.all()
    Paginas = paginasHelping.objects.all()

    for img in images:

        query = str(img.imagen)+"\""

        if not Paginas.filter(contenido__icontains=query):

            img.imagen.delete(save=True)
            img.delete()

def borrar_pdfs():

    pdfs = helpingPdf.objects.all()
    Paginas = paginasHelping.objects.all()

    for pdf in pdfs:

        query = str(pdf.pdf)+"#"

        if not Paginas.filter(contenido__icontains=query):

            pdf.pdf.delete(save=True)
            pdf.delete()

def modalEliminarAyuda(request): 

    if request.method == "POST":

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

    context = {}

    if request.method == "POST":

        if request.body:

            body = json.load(request)
            id = body['id']
            fk = body['fk']
            
            pagina=paginasHelping.objects.get(idpagina=id)
            paginas=paginasHelping.objects.filter(fk_tutorial__idtutorial=fk, ordenamiento__gte=pagina.ordenamiento)

            for pg in paginas:

                pg.ordenamiento = pg.ordenamiento - 1
                pg.save()
                
            pagina.delete()

        helping=tutoriales.objects.get(idtutorial=fk)
        paginas=paginasHelping.objects.filter(fk_tutorial__idtutorial=fk)
        context={'data': helping, 'paginas':paginas}

    html_template = (loader.get_template('Helping/modalHijosPagina.html'))
    return HttpResponse(html_template.render(context, request))

def modalPaginaMover(request): 

    context = {}

    if request.method == "POST":

        if(request.body):

            body = json.load(request)
            id = body['id']
            fk = body['fk']
            tipo = body['tipo']
            
            helping=tutoriales.objects.get(idtutorial=fk)

            if helping:

                paginas=paginasHelping.objects.filter(fk_tutorial=helping)

                if paginas and len(paginas) > 1:

                    actual = paginas.get(idpagina=id)
                    next = actual.ordenamiento - 1 if int(tipo) == 0 else actual.ordenamiento + 1
                    update = paginas.filter(Q(ordenamiento=actual.ordenamiento)|Q(ordenamiento=next))

                    if update and len(update) == 2:

                        update[0].ordenamiento = actual.ordenamiento if int(tipo) == 0 else next
                        update[0].save()
                        update[1].ordenamiento = next if int(tipo) == 0 else actual.ordenamiento
                        update[1].save()
                        paginas=paginasHelping.objects.filter(fk_tutorial=helping)
                        actual = paginas.get(idpagina=id)
                        context = {'data': helping, 'paginas':paginas, 'orden': actual}

                    else:

                        context = {'data': helping, 'paginas':paginas}

                else:

                    context = {'data': helping, 'paginas':paginas}
 
    html_template = (loader.get_template('Helping/modalHijosPagina.html'))
    return HttpResponse(html_template.render(context, request))

def validarTituloAyuda(request): 

    if request.method == "POST":

        if request.body:

            titulo = json.load(request)['titulo']
            helping = tutoriales.objects.filter(titulo=titulo)

            if not helping:
                
                return JsonResponse({'valido':'valido'})

    return HttpResponse()

    
def modalPdf(request): 

    html_template = (loader.get_template('Helping/modalPdf.html'))
    return HttpResponse(html_template.render({}, request))