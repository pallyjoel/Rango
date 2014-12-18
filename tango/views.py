from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from tango.models import Category
from django.core.context_processors import csrf
from tango.models import Page
from difflib import context_diff
from tango.forms import CategoryForm, PageForm

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
        
    c = RequestContext(request, {'form':form})
    c.update(csrf(request))
    t = loader.get_template('tango/add_category.html')
    
    return HttpResponse(t.render(c))

def add_page(request, category_name_slug):
    errors = []
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
            else:
                errors.append("cat doesn't exist")
        else:
            print form.errors
            errors.append("form is not valid")
    else:
        form = PageForm()
        errors.append("Not a Post")
    
    c = RequestContext(request, {'form':form, 'category':cat, 'slug': category_name_slug, 'errors': errors})
    c.update(csrf(request))
    t = loader.get_template('tango/add_page.html')
    
    return HttpResponse(t.render(c))    
            
def index(request):
    
    t = loader.get_template('tango/index.html')
    
    cat_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    c = Context({'categories': cat_list, 'pages': page_list})
    
    return HttpResponse(t.render(c))

def category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
        
    except Category.DoesNotExist:
        pass
            
    t = loader.get_template('tango/category.html')
    c = Context(context_dict)
    
    return HttpResponse(t.render(c))     

def about(request):
    t = loader.get_template('tango/about.html')
    c = Context({'boldmessage' : 'I am soo tired'})
    
    return HttpResponse(t.render(c))