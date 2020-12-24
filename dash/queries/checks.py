from ..forms import *
from datetime import datetime


def checks_queries(request, set_query, accounts):
    if request.method == 'POST':
        # CREAR FORMULARIO NUEVO
        form = Checks_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            amount = data.get('amount')
            req_account = request.POST['account']

            # FECHA ACTUAL
            now = datetime.now()
            date = now.strftime("%Y/%m/%d")

            # CUENTA SELECCIONADA
            selected_account = None
            for account in accounts:
                if account['id'] == req_account:
                    selected_account = account

            # VERIFICAR SALDO
            if float(selected_account['balance']) >= float(amount) and selected_account['enableChecks'] == 1:
                # QUERIES
                set_query(
                    f'INSERT INTO AccountCheck VALUES (null, "", "{date}", {amount}, {req_account}, null, 0)')


def change_checks_queries(request, set_query, fetch_query):
    if request.method == "POST":
        # CREAR FORMULARIO NUEVO
        form = Charge_Change_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data
            name = data.get('name', '')

            # VARIABLES
            account = request.POST.get('account', '')
            check = request.POST.get('check', '')

            # FECHA ACTUAL
            now = datetime.now()
            date = now.strftime("%Y/%m/%d")

            # QUERY
            user_account = fetch_query(
                f'SELECT * FROM Account WHERE id = {account}')
            account_check = fetch_query(
                f'SELECT * FROM AccountCheck WHERE id = {check} AND account = {account}')

            def change_check():
                set_query(
                    f'UPDATE Account SET debit = debit + {account_check[0][3]}, checks = checks - 1 WHERE id = {account}')
                set_query(
                    f'UPDATE AccountCheck SET charged = 1, chargedDate = "{date}", name = "{name}" WHERE id = {check}'
                )

            # VALIDAR QUE EXISTA EL CHEQUE
            if account_check and account_check[0]:
                auth_check = fetch_query(
                    f'SELECT * FROM AuthCheck WHERE id = {check}')

                # VALIDAR PRE AUTORIZACIÓN
                if user_account and user_account[0]:
                    if user_account[0][10] == 1:
                        if auth_check and auth_check[0]:
                            # ESTA PRE AUTORIZADO
                            if auth_check[0][1] == 1:
                                change_check()
                    else:
                        change_check()
