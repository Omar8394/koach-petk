from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.

def index(request):
    
    context = {'mess':'Cristo me escuchas'}
    context['segment'] = 'index'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/security/login/')
@permission_required('App.view_confmisfavoritos', login_url="/security/login/")
def Dashboard(request):
    
    context = {}
    context['segment'] = 'Dashboard'
    
    html_template = loader.get_template( 'Dashboard_Portal/Dashboard.html' )
    return HttpResponse(html_template.render(context, request))