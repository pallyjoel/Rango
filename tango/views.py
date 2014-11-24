from django.http import HttpResponse
from django.template import loader, Context


def index(request):
    
    t = loader.get_template('tango/index.html')
    c = Context({'boldmessage': "I am bold font from the context"})
    
    return HttpResponse(t.render(c))


def about(request):
    return HttpResponse("Rango says here is the about page!  <br/> <a href='/tango/'>Home</a>")
