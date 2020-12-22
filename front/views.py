from django.template.response import TemplateResponse
from django.shortcuts import redirect
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


def fetch_query(query):
    # VERIFICAR
    cursor = get_query(query)
    cursor[0].commit()

    # LISTA
    list = cursor[1].fetchall()

    # CERRAR
    cursor[1].close()
    return list


def get_user(username):
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
            "comercialName": business_user_list[0][0],
            "businessType": business_user_list[0][1],
            "name": business_user_list[0][2],
            "agent": business_user_list[0][3],
            "password": business_user_list[0][4],
            "phone": business_user_list[0][5],
        }

    return user


def renderTemplate(request, name, params={}):
    response = TemplateResponse(request, f'front/{name}.html', params)
    return response


def renderTemplate_user(request, username, name, params={}):
    user = get_user(username)
    user.update(params)
    return renderTemplate(request, name, user)


def login(request):
    # BUSCAR USUARIO
    logged = login_form(request, fetch_query)

    if logged:
        username = request.POST['username']
        return redirect(f'/accounts/{username}')

    return renderTemplate(request, 'login')


def accounts(request, username):
    user = get_user(username)
    account_res = []
    account_list = fetch_query(
        f'SELECT * FROM Account LEFT JOIN AccountType ON AccountType.id = Account.id WHERE userCui = {user["cui"]}')

    # AGREGAR SALDO
    for account in account_list:
        tmpAccount = list(account)
        tmpAccount.append(int(tmpAccount[4]) - int(tmpAccount[5]))
        account_res.append(tmpAccount)

    return renderTemplate_user(request, username, 'accounts', {
        "accounts": account_res
    })


def own_transactions(request, username):
    return renderTemplate_user(request, username, 'own_transactions')


def third_transactions(request, username):
    return renderTemplate_user(request, username, 'third_transactions')


def payments(request, username):
    return renderTemplate_user(request, username, 'payments')


def checks(request, username):
    return renderTemplate_user(request, username, 'checks')


def loans(request, username):
    return renderTemplate_user(request, username, 'loans')


def states(request, username):
    return renderTemplate_user(request, username, 'states')


def spreads(request, username):
    return renderTemplate_user(request, username, 'spreads')
