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
            if check_password(actual_password, request.user.password):
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
                    'mensaje': 'the current password entered is incorrect, please verify your password and try again to change your password',
                    'tipo': 5,
                    'titulo': 'Incorrect Password'
                }
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
    pass



@login_required(login_url="security/login/")
def securitySettings(request):
    return render(request, "securitySettings.html")

@login_required(login_url="security/login/")
def logout_view(request):
    logout(request)
    return redirect("/")

            

