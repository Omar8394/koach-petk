import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from modulesApp.App.models import AppPublico

def create_mail(user,subject, context, template_name = "base_email_template_pro.html"):
    username = ""
    message = ""
    try:
        username = AppPublico.objects.get(user_id=user.id)
        username = username.nombre +" "+ username.apellido
    except Exception as e:
        username = user.username
    try:
        template = get_template(template_name)
        content = template.render(context.update(
            {"user":username,"empresa": settings.EMPRESA_NOMBRE,
            "urlimage": settings.EMPRESA_SRC_LOGO})) #agregar empresa_email y contact
        message = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[
                settings.EMAIL_HOST_USER
            ],
            cc=[]
        )
        message.attach_alternative(content, 'text/html')
    except Exception as e:
        print("exeption ",e)
    return message

def enviar(message):
    message.send()
def send_mail(message):
    try:
        #thread = threading.Thread(target=enviar, args=(message,))
        #thread.start()
        print("enviando correo")
        enviar(message)
    except Exception as e:
        print("se ha producido un error al enviar el correo", e)