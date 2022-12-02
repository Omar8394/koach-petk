from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect("Dashboard")
    context = {'mess':'Cristo me escuchas'}
    context['segment'] = 'index'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/security/login/')
@permission_required('App.view_confmisfavoritos', login_url="/security/login/")
def Dashboard(request):
    usuario=request.user
    rol=usuario.fk_rol_usuario
    print(rol)
    context = {'rol':str(rol), 'user':usuario}
    context['segment'] = 'Dashboard'
    print(context)
    html_template = loader.get_template( 'Dashboard_Portal/Dashboard.html' )
    return HttpResponse(html_template.render(context, request))