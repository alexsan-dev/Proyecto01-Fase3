from django.template.response import TemplateResponse

# Create your views here.


def login(request):
    response = TemplateResponse(request, 'login.html', {})
    return response


def signing(request):
    response = TemplateResponse(request, 'signing.html', {})
    return response
