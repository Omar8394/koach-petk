from django.shortcuts import render,redirect,reverse

# Create your views here.
from django.views import View
from .forms import LoginForm, SignUpForm, ResetPasswordForm, RecoveryMethodForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .models import User
from .methods import es_correo_valido,change_password,get_status_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import JsonResponse
from modulesApp.App.models import ConfTablasConfiguracion

def login_view(request):
    if request.user.is_authenticated:
        return redirect("Dashboard")
    else:
         if request.method == "POST":
             form = LoginForm(request.POST or None)
             if form.is_valid():          
                username = form.cleaned_data.get("username")
                try:
                    if es_correo_valido(username):
                        username = User.objects.filter(email=username)[0].username
                except Exception as e:
                     messages.error(request, "El usuario o correo no se encuentra asocido a ninguna cuenta.")   
                password = form.cleaned_data.get("password")
                status_user = get_status_user(username, password)
                if status_user['estado'] == "Active":
                    print(status_user['mensaje'])
                    login(request, status_user['user']) 
                    return redirect("Dashboard")
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
            status_user = get_status_user(request.user, actual_password)
            if status_user['estado'] == "Active":
                change_password(request, new_password)
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
        status_user = get_status_user(request.user, actual_password)
        if status_user['estado'] == "Active":
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
    success = False
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            request.session.flush()
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                try:
                    user = User.objects.filter(email__exact=email).first()
                    ext_user = ExtensionUsuario.objects.get(user=user)
                    if ext_user.CtaUsuario.fk_status_cuenta.desc_elemento == "suspended":
                        msg = "Tu cuenta ha sido suspendida para mas informacion comunicate con el soporte."
                        success = False
                    else:
                        request.session['user_email'] = user.email
                        return redirect("/recoverymethod/")
                except Exception as e:
                    msg = "El correo ingresado no se encuentra vinculado con ninguna cuenta, o esta cuenta se encuentra bloqueada."
                    success = False
            else:
                msg = 'Form is not valid'
                success = False
        else:
            form = ResetPasswordForm()
        return render(request, "passwordreset.html",
                      {"form": form, "msg": msg, "success": success})

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
                pass
                #return redirect("/passwordReset/")
        elif request.method == "POST":
            form = RecoveryMethodForm(request.POST or None)
            if form.is_valid():
                typemethod = int(form.cleaned_data.get("typeMethod"))
                user_email = form.cleaned_data.get("email")
                if typemethod == 1:
                    ext_user = ExtensionUsuario.objects.get(
                        user__exact=User.objects.filter(email__exact=user_email).first())
                    code = str(Methods.getVerificationLink(ext_user, user_email, 2))
                    if code:
                        enlace = request.get_raw_uri().split("//")[0] + "//" + \
                                 request.get_host() + "/emailrecovery/" + code + "/"
                        context = {"titulo": "Account Recovery Request", "user": ext_user.user.username,
                                   "content": "We have received an account recovery request, to restore your account click on the following link: ",
                                   "enlace": enlace, "enlaceTexto": "click here!", "empresa": settings.EMPRESA_NOMBRE,
                                   "urlimage": settings.EMPRESA_URL_LOGO}
                        send_mail(
                            create_mail(user_email, "Account Recovery Request", "security/base_email_template_pro.html",
                                        context))
                        request.session.flush()
                        information = {"mensaje": "Te hemos enviado un enlace de recuperacion de cuenta a tu correo electronico.",
                                       "titulo": "Enlace de verificacion enviado", "urlimage": settings.EMPRESA_URL_LOGO,
                                       "imagelocal": settings.EMPRESA_SRC_LOGO}
                        return render(request, "security/information_view.html", information)
                    else:
                        print("codigo nulo")

                elif typemethod == 2:
                    request.session['user_email'] = user_email
                    return redirect("/recoverymethodquestion/")
                    pass
            else:
                #return redirect("/passwordReset/")
                pass
    return render(request, "recoverymethod.html", context)


def recovery_method_question(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.session.get("user_email"):
            email = request.session.get("user_email")
            context = {"user_email": email}
            request.session.flush()
            try:
                user = User.objects.filter(email__exact=email).first()
                ext_user = ExtensionUsuario.objects.get(user=user)
                if ext_user.CtaUsuario.fk_status_cuenta.desc_elemento == "suspended":
                    raise Http404("Esta cuenta esta suspendida, por favor contacta al soporte.")
                elif ext_user.CtaUsuario.respuesta_secreta is None:
                    information = {"mensaje": "Este metodo de recuperacion no ha sido establecido en tu cuenta.",
                                   "titulo": "Metodo no configurado", "urlimage": settings.EMPRESA_URL_LOGO,
                                   "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "security/information_view.html", information)
                else:
                    msg = None
                    if request.method == "GET":
                        request.session['user_email'] = email
                    elif request.method == "POST":
                        form = RecoveryMethodQuestion(request.POST or None)
                        if form.is_valid():
                            answer = form.cleaned_data.get("secrettext")
                            if answer == ext_user.CtaUsuario.respuesta_secreta:
                                code = str(Methods.getVerificationLink(ext_user, email, 1))
                                if code:
                                    return redirect("/emailrecovery/" + code + "/")
                                else:
                                    msg = "Error to generate code activaction"
                            else:
                                msg = "La respuesta secreta es incorrecta por favor intenta de nuevo."
                        else:
                            msg = "form invalid please fill all fields"
                    context = {"question": ext_user.CtaUsuario.fk_pregunta_secreta.desc_elemento, "msg": msg,
                               "empresa": settings.EMPRESA_NOMBRE, "urlimage": settings.EMPRESA_URL_LOGO,
                               "imagelocal": settings.EMPRESA_SRC_LOGO}
                    return render(request, "security/questionrecovery.html", context)

            except User.DoesNotExist:
                raise Http404("El correo ingresado no esta asociado a ninguna cuenta, o esta cuenta se encuentra suspendida")
        else:
            return redirect("/passwordReset/")

@login_required(login_url="security/login/")
def securitySettings(request):
    return render(request, "securitySettings.html")

@login_required(login_url="security/login/")
def logout_view(request):
    logout(request)
    return redirect("/")

            

