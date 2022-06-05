from django.shortcuts import render,redirect,reverse

# Create your views here.
from django.views import View
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import User
from .methods import es_correo_valido
from django.contrib import messages

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
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("Dashboard")
                else:
                    messages.error(request, "Usuario o contraseña invalidos")
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
                

def logout_view(request):
    logout(request)
    return redirect("/")

            

