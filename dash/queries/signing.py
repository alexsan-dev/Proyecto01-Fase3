from ..forms import *


def set_signing_queries(request, set_query):
    if request.method == 'POST':
        # CREAR FORMULARIO NUEVO
        form = SingleUser_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            cui = data.get('cui')
            nit = data.get('nit')
            name = data.get('name')
            birth = request.POST['birth'].replace('-', '/')
            username = data.get('username')
            phone = data.get('phone')
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            # QUERIES
            if (str(password) == str(confirm_password)):
                set_query(
                    f'INSERT INTO SingleUser VALUES ({cui}, {nit}, "{name}", "{birth}", "{username}", "{password}", {phone});')


def business_signing_queries(request, set_query):
    if request.method == 'POST':
        # CREAR FORMULARIO NUEVO
        form = BusinessUser_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            businessType = request.POST.get('businessType', 'Sociedad anónima')
            name = data.get('name')
            comercialName = data.get('comercialname')
            agent = data.get('agent')
            phone = data.get('phone')
            password = request.POST['password']

            # QUERIES
            set_query(
                f'INSERT INTO BusinessUser VALUES ("{comercialName}", "{businessType}", "{name}", "{agent}", "{password}", {phone});')
