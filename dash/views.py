from django.template.response import TemplateResponse
import MySQLdb

# VISTAS
from .forms.accounts import accounts_form
from .forms.signing import signing_form, business_signing_form


# CONEXIÓN A BASE DE DATOS
host = 'localhost'
db_name = 'bank'
user = 'root'
password = ''
port = 3306

# CONECTAR DB
db = MySQLdb.connect(host=host, user=user, password=password,
                     db=db_name, connect_timeout=5)

# ENVIAR TEMPLATE


def renderTemplate(request, name):
    response = TemplateResponse(request, f'dash/{name}.html', {})
    return response

# CREAR QUERY


def set_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()

# VISTA DE CUENTAS


def accounts(request):
    accounts_form(request, set_query)
    return renderTemplate(request, 'accounts')


# VISTA DE CREACIÓN DE USUARIO
def signing(request):
    signing_form(request, set_query)
    return renderTemplate(request, 'signing')

# VISTA DE CREACIÓN DE EMPRESA


def business_signing(request):
    business_signing_form(request, set_query)
    return renderTemplate(request, 'business_signing')
