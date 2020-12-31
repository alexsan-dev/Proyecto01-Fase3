from django.template.response import TemplateResponse
import MySQLdb

# VISTAS
from .queries.accounts import *
from .queries.checks import *
from .queries.signing import *
from .queries.deposits import *
from .queries.loans import *
from .queries.cards import *

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

# OBTENER QUERY


def get_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    return [db, cursor]


def fetch_query(query):
    # VERIFICAR
    cursor = get_query(query)
    cursor[0].commit()

    # LISTA
    query_list = cursor[1].fetchall()

    # CERRAR
    cursor[1].close()
    return query_list

# OBTENER CUENTAS


def get_accounts():
    accounts_list = []
    accounts = fetch_query(
        f'SELECT * FROM Account LEFT JOIN AccountType ON Account.id = AccountType.id')

    # RECORRER
    for account in accounts:
        # LISTA
        tmpAccount = list(account)

        # CALCULAR DICCIONARIO
        tmpType = "Monetaria"
        if tmpAccount[10]:
            tmpType = "Ahorro"
        elif tmpAccount[11]:
            tmpType = 'Plazo fijo'

        # CREAR DICCIONARIO
        accounts_list.append({
            "id": tmpAccount[0],
            "state": tmpAccount[1],
            "enableChecks": tmpAccount[2],
            "isSingle": tmpAccount[3],
            "credit": tmpAccount[4],
            "debit": tmpAccount[5],
            "balance": float(tmpAccount[4]) - float(tmpAccount[5]),
            "isDollar": tmpAccount[6],
            "userCui": tmpAccount[7],
            "userBusiness": tmpAccount[8],
            "type": tmpType
        })

    return accounts_list

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

# VISTA DE CHEQUES


def checks(request):
    # FORMULARIO INICIAL
    form = Checks_Form()
    accounts = get_accounts()

    render = {
        "form": form,
        "accounts": accounts
    }

    # QUERIES POST
    checks_queries(request, set_query, accounts)

    return render_template(request, 'checks', render)


# VISTA DE CHEQUES


def change_checks(request):
    # FORMULARIO INICIAL
    form = Charge_Change_Form()

    # FORMULARIO INICIAL
    accounts = get_accounts()
    checks = fetch_query(
        f'SELECT * FROM AccountCheck WHERE charged = 0')

    # QUERIES
    change_checks_queries(request, set_query, fetch_query)

    # TEMPLATE
    return render_template(request, 'change_checks', {
        "accounts": accounts,
        "checks": checks,
        "form": form
    })


def deposits(request):
    # CUENTAS
    accounts = get_accounts()

    # QUERIES
    deposits_queries(request, set_query, fetch_query)

    return render_template(request, 'deposits', {
        "accounts": accounts
    })


def loans(request):
    # PRESTAMOS
    req_loans = fetch_query(f'SELECT * FROM Loans WHERE authorized = 0')

    # VARIABLES
    render = {
        "loans": req_loans
    }

    # QUERIES
    loans_queries(request, set_query, fetch_query)

    return render_template(request, 'loans', render)


def cards(request):
    # FORMULARIO
    users = fetch_query(f'SELECT * FROM SingleUser')
    business = fetch_query(f'SELECT * FROM BusinessUser')
    accounts = fetch_query(
        f'SELECT * FROM Account LEFT JOIN AccountType ON Account.id = AccountType.id WHERE AccountType.monetary IS NOT NULL')

    all_users = users + business

    form = Cards_Form()

    # VARIABLES
    render = {
        "form": form,
        "users": all_users,
        "accounts": accounts
    }

    # QUERIES
    cards_queries(request, fetch_query, set_query)

    return render_template(request, 'cards', render)
