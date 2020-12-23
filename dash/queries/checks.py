from ..forms import *


def checks_queries(request, set_query, accounts):
    if request.method == 'POST':
        # CREAR FORMULARIO NUEVO
        form = Checks_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            name = data.get('name')
            amount = data.get('amount')
            req_account = request.POST['account']
            date = request.POST['date'].replace('-', '/')

            # CUENTA SELECCIONADA
            selected_account = None
            for account in accounts:
                if account['id'] == req_account:
                    selected_account = account

            # VERIFICAR SALDO
            if float(selected_account['balance']) >= float(amount):
                # QUERIES
                set_query(
                    f'INSERT INTO AccountCheck VALUES (null, "{name}", "{date}", {amount}, {req_account})')
                set_query(
                    f'UPDATE Account set debit = debit + {amount} WHERE id = {req_account}')
