from django.shortcuts import render,redirect,reverse, HttpResponseRedirect
import datetime
# Create your views here.
from django.views import View
from .forms import LoginForm, SignUpForm, ResetPasswordForm, RecoveryMethodForm , RecoveryMethodQuestion, \
    RecoveryMethodEmail,editProfiles
from django.contrib.auth import login, logout, update_session_auth_hash
from .models import User, CodigoVerificacion
from .methods import es_correo_valido,change_password,get_status_user, auth_user, is_user_exists, \
    send_vefication_code_email, get_verification_code , verificarenlace, create_publico, restablecer_cuenta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template import loader
from django.template.loader import render_to_string
from modulesApp.App.models import ConfTablasConfiguracion, AppPublico,ConfSettings_Atributo
from ..Organizational_network.models import nodos_grupos,nodos_gruposIntegrantes
from core import settings
from django.http import Http404
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import imghdr
from django.core.paginator import Paginator
import os
import json
from django.template.loader import render_to_string
from ..Comunication.methods import create_mail, send_mail
from django.template.defaulttags import register
@register.filter
def jsonmail(datos):
  if datos==None or datos=="" or datos=={}:
    return ""
  tlf=None
  data = json.loads(datos)

  
  if data==None or data=="" or data=={}:
      return ""
  if   'emailPrincipal' in data :
     return data['emailPrincipal']
  else:
      return ""
@register.filter
def verifica_existe_nodo(datos):
    aprob=False
    nodos=nodos_grupos.objects.get(valor_elemento="Nodo_inicial")
    integra=nodos_gruposIntegrantes.objects.filter(fk_nodogrupo=nodos,fk_public_id=datos) 
    if integra.exists():
        aprob= True
    else:
        aprob=False  
    return aprob      
def login_view(request):
    if request.user.is_authenticated:
        print()
        print(request.user)
        return redirect("Dashboard")
    else:
         
         if request.method == "POST":
             print('ko')
             print(request.user.is_authenticated)
             form = LoginForm(request.POST or None)
             if form.is_valid():          
                status_user = auth_user(form.cleaned_data.get("username"), form.cleaned_data.get("password"))
                if status_user['estado'] == "Active" or status_user['estado'] == "Active unverified":
                    
                    login(request, status_user['user']) 
                    return redirect("Dashboard")
                if status_user['estado'] == "Password expired":
                    tipo_operacion = ConfTablasConfiguracion.objects.filter(valor_elemento="tv_cambio_clave")[0]
                    code = str(get_verification_code(status_user['user'],3,tipo_operacion))
                    if code:
                        request.session['cambio_clave'] = True
                        return redirect('security:account_recovery',activation_key=str(code))
                    else:
                        messages.error(request, "Error to generate code activaction")
                else:
                    messages.error(request, status_user['estado'] +":"+ status_user['mensaje'])                           
             else:
                messages.error(request, form.errors.as_text())              
         return render(request, "index.html",{"login_show":True})
         
def register_view(request):
    login_show = False
    if request.user.is_authenticated:
        return redirect("Dashboard")
    else:    
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                if User.objects.filter(email__exact=form.cleaned_data.get('email')).count() == 0:
                   users = form.save()
                   publico=create_publico(form.cleaned_data.get('email'),users)
                   roles=User.objects.get(pk=publico.user_id_id)
                   roles.fk_rol_usuario=ConfTablasConfiguracion.objects.filter(valor_elemento="Interesado")[0]
                   roles.save()
                   tipo=ConfTablasConfiguracion.objects.filter(valor_elemento="tv_validar_cuenta")[0]
                   print(tipo)
                   nodos= nodos_grupos.objects.filter(valor_elemento="Nodo_inicial")
                   if nodos.exists():
                      nodo_inicial=nodos_gruposIntegrantes.objects.create()
                      nodo_inicial.fk_nodogrupo=nodos[0]
                      nodo_inicial.fk_public=publico
                      nodo_inicial.fecha_incorporacion=datetime.datetime.now()
                      nodo_inicial.status_integrante=ConfTablasConfiguracion.objects.get(valor_elemento='Status_activo')
                      nodo_inicial.save()
                   rango=ConfSettings_Atributo.objects.filter(valor_setting='security_verify')
                   rango_dias=ConfSettings_Atributo.objects.filter(valor_setting='security_expiracion')
                   if rango_dias.exists():
                      datos=json.loads(rango_dias.rangovalor_setting)
                   if rango.exists():
                    if rango[0].status_setting == 1:
                      code = str(get_verification_code(users,int(datos['max']),tipo))
                      enlace = request.get_raw_uri().split("//")[0] + "//" + \
                               request.get_host() + "/verificationaccount/" + code + "/"
                      context = {"titulo": "Account Verification", "user": users,
                                 "content": "Thank you for joining the " + str(
                                   settings.EMPRESA_NOMBRE) + " team, to verify your account click on the following link: ",
                                 "enlace": enlace, "enlaceTexto": "click here!", "informacion": 'informacion.descripcion',
                                 "empresa": settings.EMPRESA_NOMBRE,
                                 "urlimage": settings.EMPRESA_SRC_LOGO, "empresa_contact": 'settings.EMPRESA_CONTACT_PAGE',
                                 "empresa_email": 'settings.'}
                      print(context)
                      send_mail(
                       create_mail(users, "Account Verification Request", "security/base_email_template_pro.html",
                                context))
                      information = {
                       "mensaje": "Le hemos enviado un enlace de verificación de cuenta al correo electrónico proporcionado. Recuerda revisar la carpeta de spam",
                       "titulo": "El enlace de registro ha sido enviado", "urlimage": settings.EMPRESA_SRC_LOGO,
                       "imagelocal": settings.EMPRESA_SRC_LOGO}
                      return render(request, "information_view.html", information)
                    else:
                       messages.success(request, "Te has registrado con exito inicia session para ingresar.")
                       login_show = True
            else:
                messages.error(request, form.errors.as_text())
    return render(request, "index.html",{"login_show":login_show})
def verificationaccount(request, activation_key):
    try:
        enlace = CodigoVerificacion.objects.get(activation_key=activation_key)
        if enlace.usuario.CtaUsuario.fk_status_cuenta != "suspend":
            if verificarenlace(enlace.key_expires):
                print("enlace valido", activation_key)
                context = {"user": enlace.usuario.user.username}
                if request.method == "GET":
                    restablecer_cuenta(enlace)
                    login(request, enlace.usuario.user)
                    return redirect("/registration/enrollment/")
            else:
                information = {"mensaje": "El enlace que estas intentando usar ha expirado por favor solicita otro.",
                               "titulo": "Enlace Expirado", "urlimage": settings.EMPRESA_URL_LOGO,
                               "imagelocal": settings.EMPRESA_SRC_LOGO}
                return render(request, "security/information_view.html", information)
        else:
            information = {"mensaje": "Esta cuenta de usuario se encuentra bloqueada por favor comunicate con el soporte.",
                           "titulo": "Cuenta Bloqueada", "urlimage": settings.EMPRESA_URL_LOGO,
                           "imagelocal": settings.EMPRESA_SRC_LOGO}
            return render(request, "information_view.html", information)
    except CodigoVerificacion.DoesNotExist:
        information = {"mensaje": "El enlace que estas intentando usar es invalido o ha expirado."+
            "\n Los enlaces de verificacion enviados a tu correo son de un solo uso por tanto no se pueden reutilizar,\n"+
            "si estas intentando verificar tu cuenta es posible que ya este verificada verificalo iniciando sesion, \n"+
            "si buscas recuperar tu cuenta intenta realizar el proceso nuevamente asegurandote de abrir en enlace una vez de forma correcta,\n"+
            "aun asi si el problema persiste o piensas que esto es un error comunicate a nuestros canales de soporte.",
                       "titulo": "Enlace Invalido", "urlimage": settings.EMPRESA_URL_LOGO,
                       "imagelocal": settings.EMPRESA_SRC_LOGO}
        return render(request, "information_view.html", information)

 
@login_required(login_url="security/login/")
def changePassword(request):
    if request.method == 'POST':
        actual_password = request.POST.get('password')
        new_password = request.POST.get('password1')
        # verificar encriptacion
        if actual_password != new_password:
            status_user = auth_user(str(request.user), str(actual_password))
            if status_user['estado'] == "Active" or status_user['estado'] == "Active unverified"\
                or status_user['estado'] == "Password expired":
                change_password(request,status_user['user'], new_password)
                response = {
                    'mensaje': 'Your password has been changed correctly',
                    'tipo': 4,
                    'titulo': 'Password changed successfully',
                    'code': 'changed'
                }
                # operacion = TablasConfiguracion.objects.get(valor_elemento='change_passsword')
                # modulo = TablasConfiguracion.objects.get(valor_elemento='module_security')
                # descripcion = "Not Adiccional data!!!"
                # LogSeguridad.objects.create(fecha_transaccion=datetime.today(), fk_cta_usuario=request.user,
                #                             fk_tipo_operacion=operacion, modulo=modulo, valor_dato=descripcion)
            else:
                response = {
                    'mensaje': status_user["mensaje"],
                    'tipo': 5,
                    'titulo': status_user["estado"]
                }
                if status_user["estado"] == "Account Blocked" or status_user["estado"] == "Account Suspended":
                    logout(request)
        else:
            response = {
                'mensaje': 'the password you want to change cannot be the same as the current password', 'tipo': 5,
                'titulo': 'Same password'
            }
        return JsonResponse(response)
    elif request.method == 'GET':
        return render(request, "cambiarclave.html")
    
@login_required(login_url="security/login/")
def changeSecretQuestion(request):
    user = request.user
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        id_pregunta = request.POST.get('cb_tipo_pregunta')
        actual_password = request.POST.get('password')
        # verificar encriptacion
        status_user = auth_user(str(request.user), str(actual_password))
        if status_user['estado'] == "Active" or status_user['estado'] == "Active unverified"\
            or status_user['estado'] == "Password expired":
            user.fk_pregunta_secreta_id = id_pregunta
            user.respuesta_secreta = respuesta
            user.save()
            response = {
                'mensaje': 'Your secret question has been changed correctly',
                'tipo': 4,
                'titulo': 'Secret question changed successfully',
                'code': 'changed'
            }
            #operacion = TablasConfiguracion.objects.get(valor_elemento='change_secret_question')
            #modulo = TablasConfiguracion.objects.get(valor_elemento='module_security')
            #descripcion = "Not Adiccional data!!!"
            #LogSeguridad.objects.create(fecha_transaccion=datetime.today(), fk_cta_usuario=request.user,
                                        #fk_tipo_operacion=operacion, modulo=modulo, valor_dato=descripcion)
        else:
            response = {
                    'mensaje': status_user["mensaje"],
                    'tipo': 5,
                    'titulo': status_user["estado"]
                }
            if status_user["estado"] == "Account Blocked" or status_user["estado"] == "Account Suspended":
                    logout(request)

        return JsonResponse(response)
    elif request.method == 'GET':
        tipo_pregunta = ConfTablasConfiguracion.obtenerHijos("pregSecreta")
        context = {'preguntas': tipo_pregunta, 'pregunta_id': user.fk_pregunta_secreta_id,
                   'respuesta': user.respuesta_secreta}
        return render(request, "cambiarpregunta.html", context)
    
def forgot_password(request):
    msg = None
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            request.session.flush()
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email") # or user valida ambos
                status_user = get_status_user(email)
                if status_user['estado'] != "Account Suspended" and status_user['estado'] != "Invalid Account":
                    request.session['user_email'] = status_user['user'].email
                    return redirect("security:recovery_method")
                else:
                    msg = status_user['mensaje']
            else:
                msg = 'Form is not valid'
        else:
            form = ResetPasswordForm()
        return render(request, "passwordreset.html",
                      {"form": form, "msg": msg})

def recovery_method(request):
    context = None
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "GET":
            if request.session.get("user_email"):
                context = {"user_email": request.session.get("user_email")}
                request.session.flush()
            else:
                return redirect("security:forgot_password")
        elif request.method == "POST":
            form = RecoveryMethodForm(request.POST or None)
            if form.is_valid():
                typemethod = int(form.cleaned_data.get("typeMethod"))
                user_email = form.cleaned_data.get("email")
                if typemethod == 1:
                    user = is_user_exists(user_email)
                    tipo_operacion = ConfTablasConfiguracion.objects.filter(valor_elemento="tv_recuperar_cuenta")[0]
                    send_vefication_code_email(user, "Account Recovery Code", None, tipo_operacion)
                    request.session.flush()
                    information = {"mensaje": "Te hemos enviado un enlace de recuperacion de cuenta a tu correo electronico.",
                                       "titulo": "Enlace de verificacion enviado",
                                       "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "information_view.html", information)

                elif typemethod == 2:
                    request.session['user_email'] = user_email
                    return redirect("security:recovery_method_question")
            else:
                return redirect("security:forgot_password")
    return render(request, "recoverymethod.html", context)


def recovery_method_question(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        status_user = None
        if request.session.get("user_email"):
            email = request.session.get("user_email")
            context = {"user_email": email}
            request.session.flush()
            status_user = get_status_user(email)
            if status_user['estado'] == "Account Suspended" or status_user['estado'] == "Invalid Account":
                information = {"mensaje": status_user['mensaje'],
                                "titulo": status_user['estado'],
                                "imagelocal": settings.EMPRESA_SRC_LOGO}
                return render(request, "information_view.html", information)
            elif status_user['user'].respuesta_secreta is None:
                information = {"mensaje": "Este metodo de recuperacion no ha sido establecido en tu cuenta.",
                                "titulo": "Metodo no configurado",
                                "imagelocal": settings.EMPRESA_SRC_LOGO}
                return render(request, "information_view.html", information)
            else:
                msg = None
                if request.method == "GET":
                    request.session['user_email'] = email
                elif request.method == "POST":
                    form = RecoveryMethodQuestion(request.POST or None)
                    if form.is_valid():
                        answer = form.cleaned_data.get("secrettext")
                        if answer == status_user['user'].respuesta_secreta:
                            tipo_operacion = ConfTablasConfiguracion.objects.filter(valor_elemento="tv_recuperar_cuenta")[0]
                            code = str(get_verification_code(status_user['user'],3,tipo_operacion))
                            if code:
                                return redirect('security:account_recovery',activation_key=str(code))
                            else:
                                msg = "Error to generate code activaction"
                        else:
                            msg = "La respuesta secreta es incorrecta por favor intenta de nuevo."
                    else:
                        msg = "form invalid please fill all fields"
                context = {"question": status_user['user'].fk_pregunta_secreta.desc_elemento, "msg": msg,
                            "empresa": settings.EMPRESA_NOMBRE,
                            "imagelocal": settings.EMPRESA_SRC_LOGO}
                return render(request, "questionrecovery.html", context)
        else:
            return redirect("security:forgot_password")
        
def account_recovery(request, activation_key):
    try:
        cambio_clave = "Solicitud de Recuperacion de Cuenta"
        boton_submit = "Recuperar Cuenta"
        if request.session.get("cambio_clave"):
            boton_submit = "Cambiar Contraseña"
            cambio_clave = "Tu Contraseña ha Caducado!"
        enlace = CodigoVerificacion.objects.get(activation_key=activation_key)
        if enlace.usuario.fk_status_cuenta.valor_elemento != "user_account_suspended":
            if verificarenlace(enlace.activation_key):
                print("enlace valido", activation_key)
                context = {"user": enlace.usuario.username,
                           "imagelocal": settings.EMPRESA_SRC_LOGO, "cambioclave": cambio_clave, "botonsubmit": boton_submit}
                if request.method == "POST":
                    form = RecoveryMethodEmail(request.POST or None)
                    if form.is_valid():
                        print("form is valid and key link is valid")
                        change_password(None, enlace.usuario, form.cleaned_data['password1'],enlace)
                        '''operacion = TablasConfiguracion.objects.get(valor_elemento='recovery_account_email')
                        modulo = TablasConfiguracion.objects.get(valor_elemento='module_security')
                        descripcion = "Activation key " + activation_key
                        LogSeguridad.objects.create(fecha_transaccion=datetime.today(),
                                                    fk_cta_usuario=enlace.usuario.user,
                                                    fk_tipo_operacion=operacion, modulo=modulo, valor_dato=descripcion)'''
                        messages.success(request, "Your credentials have been changed correctly, try to login")
                        return redirect("security:login")
                    else:
                        print("invalid form")
            else:
                raise Http404("This link has expired please request another link")
        else:
            raise Http404("This account is locked, please contact support")
    except CodigoVerificacion.DoesNotExist:
        raise Http404("This verification link is invalid or has expired")
    return render(request, "emailrecovery.html", context)
def review_new_register(request):
    rol=ConfTablasConfiguracion.objects.get(valor_elemento="Interesado") 
    integrantes=AppPublico.objects.filter(user_id__fk_rol_usuario=rol)
    nodos=nodos_grupos.objects.get(valor_elemento="Nodo_inicial")
    idPersona=None
    is_cookie_set = 0
    if 'idPersona' in request.session:
        idPersona=request.session['idPersona'] if 'idPersona' in request.session else None  
        is_cookie_set = 1
    if request.method == "GET":
       if request.GET.get('page')==None: 
          is_cookie_set = 0 
          request.session['idPersona']=None
          idPersona=None
       if (is_cookie_set == 1):
          if idPersona!=None and idPersona!="":
              integrantes=integrantes.filter(nombre__icontains=idPersona)
    if request.method == "POST":
        print('hola')        
        if (is_cookie_set == 1):          
          request.session['idPersona']=None 
        idPersona=request.POST.get('PersonId')
        print(request.POST)
        if idPersona != None and idPersona!="" :
            
           integrantes=integrantes.filter(nombre__icontains=idPersona) 
           request.session['PersonId'] = idPersona             
    paginator = Paginator(integrantes, 10)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'matriculasList': page_obj,'integrantes':integrantes,'gruposi':nodos.pk}
    html_template = (loader.get_template('new_register_review.html'))
    return HttpResponse(html_template.render(context, request))   

@login_required(login_url="security/login/")
def securitySettings(request):
    return render(request, "securitySettings.html")

@login_required(login_url="security/login/")
def logout_view(request):
    logout(request)
    return redirect("/")


def images(request):
    if request.method == "POST":

        myfile = request.FILES['file-input']

        fs = FileSystemStorage(location=settings.UPLOAD_ROOT)
        nombreImagen = str(request.user.id) + ".png"
        Ruta = settings.UPLOAD_ROOT + '/user'
        RutaUrl = settings.UPLOAD_URL + '/user'
        try:

            os.mkdir(os.path.join(Ruta))

        except:
    
            pass

        fs.delete(Ruta + '/' + nombreImagen)
        fs.save(Ruta + '/' + nombreImagen, myfile)

        ctauser = User.objects.filter(id=request.user.id).first()
        if ctauser:
            ctauser.url_imagen=nombreImagen
            ctauser.save()

        return JsonResponse({'mensaje': 'Changes applied successfully', 'ruta': (RutaUrl + '/' + nombreImagen)})

def rootImages(request):
    if request.method == "POST":

        ctauser = User.objects.filter(id=request.user.id).first()

        if (ctauser.url_imagen):

            Ruta = settings.UPLOAD_URL + 'user/' + ctauser.url_imagen if ctauser else None
            root = settings.UPLOAD_ROOT + '/user/' + ctauser.url_imagen if ctauser else None

            if not os.path.exists(root):
                Ruta = None

        else:

            Ruta = None
            root = None

    response = {
        'ruta': Ruta
    }

    return JsonResponse(response)


def borrarImages(request):
    if request.method == "POST":
        ctauser = User.objects.filter(id=request.user.id).first()
        if ctauser.url_imagen and ctauser.url_imagen != '':

            fs = FileSystemStorage(location=settings.UPLOAD_ROOT)
            nombreImagen = ctauser.url_imagen
            Ruta = settings.UPLOAD_ROOT + '/user'

            fs.delete(Ruta + '/' + nombreImagen)

            if ctauser:
                ctauser.url_imagen=url_imagen=None
                ctauser.save()

            return JsonResponse({'mensaje': 'Image deleted'})

        else:

            return JsonResponse({'mensaje': 'There is no image to remove'})
        
def editProfile(request):
    btn_next = "activo"
    nuevo = None
    try:
        nuevo = AppPublico.objects.get(user_id=request.user)

    except:
        pass      
    if not nuevo:
        nuevo = AppPublico.objects.create()
        nuevo.user_id = request.user
        nuevo.save()

    profile = nuevo
    telefono = profile.telefono_principal
    correo = profile.correo_principal
    img = nuevo.user_id.url_imagen
    if request.method == "POST":

        form = editProfiles(request.POST, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)       
            form.save()
            messages.info(request, 'Changes applied successfully')
            return render(request, "profilePage.html", {'form': form, 'telefono_principal': None if not telefono else telefono,
                                                         'img': img if img and img != "" else None})

        else:
            print(form.errors)
            messages.warning(request, 'An error has occurred!')
            return render(request, "profilePage.html", {'form': form, 'telefono_principal': None if not telefono else telefono,
                                                         'img': img if img and img != "" else None})

    form = editProfiles(instance=profile, initial={'telefono_principal':None if not telefono else telefono,
                                                   'correo_principal': None if not correo else correo})
    return render(request, "profilePage.html", {'form': form,
                                                         'telefono_principal': None if not telefono else telefono,
                                                         'img': img if img and img != "" else None})
    
def renderListasCombos(request):

    clave = request.POST.get('clave', None)
    tipo = request.POST.get('tipo', None)
    print(tipo)
    
    if(tipo and clave and tipo == 'TablasConfiguracion'):

        lista = ConfTablasConfiguracion.obtenerHijos('countries_iso' if clave == 'pais' else '')

    if(tipo and clave and tipo == 'Perfil'):

        lista = Perfil.objects.all()


    if(tipo and clave and tipo == 'Publico'):

        lista = Publico.objects.all()

    html = render_to_string('Planning/comboFiltro.html', {'lista': lista, 'tipo': tipo})

    response = {

        'lista': html

    }

    return JsonResponse(response)

def testvue(request):
    return render(request, "testVue.html")

def testdata(request):
    return JsonResponse({"hola":"hola mundo"})

def Modaltransfersec(request):
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
         try:
            if request.body:
                context={}
                title=False
                data = json.load(request)
                print(data)
                if data["method"] == "Show":
                    print(data)
                    grupos=nodos_grupos.objects.filter(fk_grupoNodo_padre_id=None,status_grupo=60)
                    context = {'grupos':grupos}
                    html_template = (loader.get_template('modaltransfer.html'))
                    return HttpResponse(html_template.render(context, request)) 
                elif data['method'] == "Create":
                     print(data)
                     
                     grupo_transfer=nodos_gruposIntegrantes.objects.get(fk_public=data['tipo'])
                     grupo_transfer.fk_nodogrupo_id=data['data']['categoryProgram']
                     grupo_transfer.save()
                     publico=AppPublico.objects.get(pk=data['tipo'])
                     user_rol= User.objects.get(pk=publico.user_id_id)
                     user_rol.fk_rol_usuario=ConfTablasConfiguracion.objects.filter(valor_elemento="Estudiante")[0]
                     user_rol.save()
                     return JsonResponse({"message":"ok"})
         except Exception as e:
               print(e)
               return JsonResponse({"message":"error"}, status=500)              

