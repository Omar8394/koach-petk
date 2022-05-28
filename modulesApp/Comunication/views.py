from django.http import HttpResponse
from django.template import loader


# Create your views here.

# codigo para crear-actualizar-mostrar boletin-info

def createBoletin(request):
    pass
    context = {}

    html_template = loader.get_template( 'Comunication/Boletin/createBoletin.html' )
    return HttpResponse(html_template.render(context, request))

def addBoletinModal(request):
    context = {}

    if request.method == "POST": 

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:

                html_template = loader.get_template( 'Comunication/Boletin/addBoletinModal.html' )
                return HttpResponse(html_template.render(context, request))

def showBoletin(request):
    context = {}

    if request.method == "POST": 

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            if request.body:

                html_template = loader.get_template( 'Comunication/Boletin/showBoletin.html' )
                return HttpResponse(html_template.render(context, request))

# endblock boletin-info
    