# DJANGO
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.shortcuts import redirect

# FORMULARIOS
from .queries.login import *

# MYSQL
import MySQLdb

# CONEXIÓN A BASE DE DATOS
host = 'localhost'
db_name = 'bank'
user = 'root'
password = ''
port = 3306

# CONECTAR DB
db = MySQLdb.connect(host=host, user=user, password=password,
                     db=db_name, connect_timeout=5)


def renderTemplate(request, name, params={}):
    response = TemplateResponse(request, f'shop/{name}.html', params)
    return response


def get_user(request):
    # LEER USUARIO
    username = request.session['shop_auth']['username']

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

# RENDERIZAR TEMPLATE CON USUARIO


def renderTemplate_user(request, name, params={}):
    if request.session['auth']:
        user = get_user(request)
        user.update(params)
        return renderTemplate(request, name, user)

    else:
        return redirect('/shop/login')


# OBTENER QUERY


def get_query(query):
    cursor = db.cursor()
    cursor.execute(query)
    return [db, cursor]

# FETCH QUERY


def fetch_query(query):
    # VERIFICAR
    cursor = get_query(query)
    cursor[0].commit()

    # LISTA
    query_list = cursor[1].fetchall()

    # CERRAR
    cursor[1].close()
    return query_list

# LOGIN


def login(request):
    # BUSCAR USUARIO
    logged = login_queries(request, fetch_query)

    # SE ENCONTRÓ EL USUARIO
    if logged:
        username = request.POST['username']
        password = request.POST['password']

        # GUARDAR EN SESION
        request.session['shop_auth'] = {
            "username": username,
            "password": password
        }

        # REDIRECT
        return redirect(f'/shop/store')

    # RENDER
    return renderTemplate(request, 'login')


def store(request):
    return renderTemplate_user(request, 'store')
