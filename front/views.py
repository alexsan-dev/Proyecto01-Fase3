from django.template.response import TemplateResponse

# Create your views here.


def renderTemplate(request, name):
    response = TemplateResponse(request, f'{name}.html', {})
    return response


def login(request):
    return renderTemplate(request, 'login')


def signing(request):
    return renderTemplate(request, 'signing')


def business_signing(request):
    return renderTemplate(request, 'business_signing')


def accounts(request):
    return renderTemplate(request, 'accounts')


def own_transactions(request):
    return renderTemplate(request, 'own_transactions')


def third_transactions(request):
    return renderTemplate(request, 'third_transactions')


def payments(request):
    return renderTemplate(request, 'payments')


def checks(request):
    return renderTemplate(request, 'checks')


def loans(request):
    return renderTemplate(request, 'loans')


def admin(request):
    return renderTemplate(request, 'admin')
