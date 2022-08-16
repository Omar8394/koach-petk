from django.http import HttpResponse
from django.template import loader
from .methods import create_mail, send_mail

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

def emailTest(request):
    context = {"titulo": "Account Registration Link", "user": "publico.nombre" + " " + "publico.apellido",
                                "content": "Thank you for joining the " + 
                                    "settings.EMPRESA_NOMBRE" + " team, follow the link below to register  your account:",
                                "enlace": "enlace", "enlaceTexto": "click here!", "empresa": "settings.EMPRESA_NOMBRE",
                                "urlimage": "settings.EMPRESA_URL_LOGO"}
    send_mail(create_mail("tadifred@gmail.com", "Account Registration Link", "base_email_template_pro.html",
                                        context))
    return HttpResponse("fine")