from django.shortcuts import render,redirect,reverse, HttpResponseRedirect

# Create your views here.
from django.views import View
from .forms import LoginForm, SignUpForm, ResetPasswordForm, RecoveryMethodForm , RecoveryMethodQuestion, \
    RecoveryMethodEmail
from django.contrib.auth import login, logout, update_session_auth_hash
from .models import User, CodigoVerificacion
from .methods import es_correo_valido,change_password,get_status_user, auth_user, is_user_exists, \
    send_vefication_code_email, get_verification_code , verificarenlace
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import JsonResponse
from modulesApp.App.models import ConfTablasConfiguracion
from core import settings
from django.http import Http404

def login_view(request):
    if request.user.is_authenticated:
        return redirect("Dashboard")
    else:
         if request.method == "POST":
             form = LoginForm(request.POST or None)
             if form.is_valid():          
                status_user = auth_user(form.cleaned_data.get("username"), form.cleaned_data.get("password"))
                if status_user['estado'] == "Active" or status_user['estado'] == "Active unverified":
                    print(status_user['mensaje'])
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
                user = form.save()
                messages.success(request, "Te has registrado con exito inicia session para ingresar.")
                login_show = True
            else:
                messages.error(request, form.errors.as_text())
    return render(request, "index.html",{"login_show":login_show})
 
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

@login_required(login_url="security/login/")
def securitySettings(request):
    return render(request, "securitySettings.html")

@login_required(login_url="security/login/")
def logout_view(request):
    logout(request)
    return redirect("/")

            

