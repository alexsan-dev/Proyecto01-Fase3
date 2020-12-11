from django.template.response import TemplateResponse

# Create your views here.


def index(request):
    response = TemplateResponse(request, 'index.html', {})
    return response
