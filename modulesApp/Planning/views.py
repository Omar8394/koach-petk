from django.http import HttpResponse
from django.template import loader


# Create your views here.

def func_Planning(request): 
    context = {}

    html_template = loader.get_template( 'Planning/carpPlanning/crear_ficha.html' )
    return HttpResponse(html_template.render(context, request))
def render_fihas(request): 
    context = {}

    html_template = loader.get_template( 'Planning/renderfihas.html' )
    return HttpResponse(html_template.render(context, request))
    
    
               
                
