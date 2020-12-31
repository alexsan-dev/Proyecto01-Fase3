from django.template.response import TemplateResponse
from django.shortcuts import redirect
import MySQLdb

# FORMULARIOS
from .queries.login import *
from .queries.transactions import *
from .queries.accounts import *
from .queries.checks import *
from .queries.spreads import *
from .queries.cards import *
from .queries.loans import *

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

# LEER QUERY


def fetch_query(query):
    # VERIFICAR
    cursor = get_query(query)
    cursor[0].commit()

    # LISTA
    query_list = cursor[1].fetchall()

    # CERRAR
    cursor[1].close()
    return query_list

# OBTENER USUARIO


def get_user(request):
    # LEER USUARIO
    username = request.session['auth']['username']

    # LEER USUARIOS
    user_list = fetch_query(
        f'SELECT * FROM SingleUser WHERE username = "{username}"')
    business_user_list = fetch_query(
        f'SELECT * FROM BusinessUser WHERE comercialName = "{username}"')

    # VERIFICAR
    user = None

    if len(user_list) > 0:
        user = {
            "cui": user_list[0][0],
            "nit": user_list[0][1],
            "name": user_list[0][2],
            "birth": user_list[0][3],
            "username": user_list[0][4],
            "password": user_list[0][5],
            "phone": user_list[0][6]
        }
    elif len(business_user_list) > 0:
        user = {
            "username": business_user_list[0][0],
            "comercialName": business_user_list[0][0],
            "businessType": business_user_list[0][1],
            "name": business_user_list[0][2],
            "agent": business_user_list[0][3],
            "password": business_user_list[0][4],
            "phone": business_user_list[0][5],
        }

    return user

# RENDERIZAR TEMPLATE


def renderTemplate(request, name, params={}):
    response = TemplateResponse(request, f'front/{name}.html', params)
    return response

# RENDERIZAR TEMPLATE CON USUARIO


def renderTemplate_user(request, name, params={}):
    if request.session['auth']:
        user = get_user(request)
        user.update(params)
        return renderTemplate(request, name, user)

    else:
        return redirect('/login')

# LEER TODAS LAS CUENTAS


def get_third_accounts(request):
    # OBTENER CUENTAS
    user = get_user(request)
    userCui = user.get("cui", "")
    userBusiness = user.get("comercialName", "")

    # FETCH
    third_accounts = []
    third_accounts_list = fetch_query(
        f'SELECT * FROM ThirdAccount WHERE userCui = {userCui} OR userBusiness = "{userBusiness}"')

    for third_account in third_accounts_list:
        tmpAccount = list(third_account)
        third_accounts.append({
            "id": tmpAccount[0],
            "userCui": tmpAccount[1],
            "userBusiness": tmpAccount[2],
            "thirdCui": tmpAccount[3],
            "thirdBusiness": tmpAccount[4],
            "type": tmpAccount[5]
        })

    # RETURN
    return third_accounts


def get_accounts(request):
    # OBTENER CUENTAS
    user = get_user(request)
    userCui = user.get("cui", "")
    userBusiness = user.get("comercialName", "")

    account_res = []
    account_list = fetch_query(
        f'SELECT * FROM Account LEFT JOIN AccountType ON AccountType.id = Account.id WHERE userCui = "{userCui}" OR userBusiness = "{userBusiness}"')

    # AGREGAR SALDO
    for account in account_list:
        # LISTA
        tmpAccount = list(account)

        # CALCULAR DICCIONARIO
        tmpType = "Monetaria"
        if tmpAccount[12]:
            tmpType = "Ahorro"
        elif tmpAccount[13]:
            tmpType = 'Plazo fijo'

        # CREAR DICCIONARIO
        account_res.append({
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

    # RETORNAR
    return account_res

# VISTA DE LOGIN


def login(request):
    # BUSCAR USUARIO
    logged = login_queries(request, fetch_query)

    # SE ENCONTRÓ EL USUARIO
    if logged:
        username = request.POST['username']
        password = request.POST['password']

        # GUARDAR EN SESION
        request.session['auth'] = {
            "username": username,
            "password": password
        }

        # REDIRECT
        return redirect(f'/accounts/')

    # RENDER
    return renderTemplate(request, 'login')

# VISTA DE CUENTAS


def accounts(request):
    # OBTENER CUENTAS
    accounts = get_accounts(request)
    user = get_user(request)

    # FORMULARIO INICIAL
    form = ThirdAccount_Form()
    render = {
        "form": form,
        "accounts": accounts
    }

    # QUERIES
    accounts_queries(request, fetch_query, set_query, user)

    # RENDER
    return renderTemplate_user(request, 'accounts', render)

# VISTA DE TRANSACCIONES


def own_transactions(request):
    # OBTENER CUENTAS
    accounts = get_accounts(request)

    # FORMULARIO INICIAL
    form = Transactions_Form()
    render = {
        "form": form,
        "accounts": accounts
    }

    # POST DE TRANSACCION
    transactions_queries(request, get_accounts, set_query, fetch_query)

    # RENDER
    return renderTemplate_user(request, 'own_transactions', render)


def third_transactions(request):
    # OBTENER CUENTAS
    accounts = get_accounts(request)
    third_accounts = get_third_accounts(request)

    # FORMULARIO INICIAL
    form = Transactions_Form()
    render = {
        "form": form,
        "accounts": accounts,
        "third_accounts": third_accounts
    }

    # POST DE TRANSACCION
    transactions_queries(request, get_accounts, set_query, fetch_query)

    return renderTemplate_user(request, 'third_transactions', render)


def payments(request):
    return renderTemplate_user(request, 'payments')


def checks(request):
    # OBTENER USUARIO
    user = get_user(request)
    cui = user.get('cui', 0)
    userBusiness = user.get('comercialName', '')

    # CUENTAS
    accounts = get_accounts(request)

    # OBTENER CHEQUES
    checks_queries(request, set_query, fetch_query)
    checks = fetch_query(
        f'SELECT * FROM Account RIGHT JOIN Accountcheck ON Accountcheck.account = Account.id WHERE userCui = {cui} OR userBusiness = "{userBusiness}"')

    return renderTemplate_user(request, 'checks', {
        "checks": checks,
        "accounts": accounts
    })


def loans(request):
    # FORMULARIO
    form = Loans_Form()
    user = get_user(request)
    accounts = get_accounts(request)
    cui = user.get('cui', 0)
    userBusiness = user.get('comercialName', '')

    loans = fetch_query(
        f'SELECT * FROM LoanQuotas INNER JOIN Loans WHERE LoanQuotas.loan = Loans.id AND LoanQuotas.payDate is null AND Loans.userBusiness = "{userBusiness}" OR Loans.userCui = {cui}')

    # VARIABLES
    render = {
        "user": user,
        "form": form,
        "quotas": None,
        "accounts": accounts,
        "loans": loans
    }

    # QUERIES
    if request.method == 'POST':
        render = loans_queries(request, set_query, fetch_query, render, user)
        loan_quotas_queries(request, set_query, fetch_query)

    return renderTemplate_user(request, 'loans', render)


def states(request):
    # CUENTAS
    accounts = get_accounts(request)

    # QUERIES
    auth_checks_queries(request, set_query, fetch_query)

    return renderTemplate_user(request, 'states', {
        "accounts": accounts
    })


def spreads(request):
    # CUENTAS
    accounts = get_accounts(request)
    user = get_user(request)

    # PLANILLAS
    spreads = fetch_query(
        f'SELECT * FROM SpreadsPay LEFT JOIN Account ON SpreadsPay.account = Account.id WHERE SpreadsPay.userBusiness = "{user["comercialName"]}"')

    # FORMULARIO INICIAL
    form = Spreads_Form()
    render = {
        "form": form,
        "accounts": accounts,
        "spreads": spreads,
        "user": user
    }

    # QUERIES
    spreads_queries(request, user, set_query, fetch_query)

    return renderTemplate_user(request, 'spreads', render)


def cards(request):
    user = get_user(request)
    userCui = user.get('cui', 0)
    userBusiness = user.get('comercialName', '')
    cards = fetch_query(
        f'SELECT * FROM Cards WHERE userCui = {userCui} OR userBusiness = "{userBusiness}"')

    render = {
        "cards": cards
    }

    if request.method == 'POST':
        render = cards_queries(request, fetch_query, render)

    return renderTemplate_user(request, 'cards', render)
