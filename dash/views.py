from django.template.response import TemplateResponse
import MySQLdb

# VISTAS
from .queries.accounts import *
from .queries.signing import *

# FORM MODELS
from .forms import *


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


def render_template(request, name, params={}):
    response = TemplateResponse(request, f'dash/{name}.html', params)
    return response

# CREAR QUERY


def set_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()

# VISTA DE CUENTAS


def accounts(request):
    # FORMULARIO INICIAL
    form = Account_Form()
    render = {
        "form": form
    }

    # RECUPERAR
    set_accounts_queries(request, set_query)

    # RENDER
    return render_template(request, 'accounts', render)


# VISTA DE CREACIÓN DE USUARIO
def signing(request):
    # FORMULARIO INICIAL
    form = SingleUser_Form()
    render = {
        "form": form,
    }

    # RECUPERAR
    set_signing_queries(request, set_query)
    return render_template(request, 'signing', render)

# VISTA DE CREACIÓN DE EMPRESA


def business_signing(request):
    # FORMULARIO INICIAL
    form = BusinessUser_Form()
    render = {
        "form": form,
    }

    # RECUPERAR
    business_signing_queries(request, set_query)
    return render_template(request, 'business_signing', render)
