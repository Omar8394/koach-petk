from django.shortcuts import render,redirect,reverse

# Create your views here.
from django.views import View
from .forms import LoginForm, SignUpForm
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

@login_required(login_url="security/login/")
def securitySettings(request):
    return render(request, "securitySettings.html")

@login_required(login_url="security/login/")
def logout_view(request):
    logout(request)
    return redirect("/")

            

