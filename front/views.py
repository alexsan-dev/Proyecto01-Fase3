from django.template.response import TemplateResponse
import MySQLdb

from .forms.login import login_form


# CONEXIÓN A BASE DE DATOS
host = 'localhost'
db_name = 'bank'
user = 'root'
password = ''
port = 3306

# CONECTAR DB
db = MySQLdb.connect(host=host, user=user, password=password,
                     db=db_name, connect_timeout=5)

# CREAR QUERY


def set_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()


def get_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    return [db, cursor]


def renderTemplate(request, name):
    response = TemplateResponse(request, f'front/{name}.html', {})
    return response


def login(request):
    # BUSCAR USUARIO
    logged = login_form(request, get_query)

    # LOGIN
    if logged:
        return renderTemplate(request, 'accounts')

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


def states(request):
    return renderTemplate(request, 'states')


def spreads(request):
    return renderTemplate(request, 'spreads')
