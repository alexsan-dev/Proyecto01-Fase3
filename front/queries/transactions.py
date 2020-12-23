from ..forms import Transactions_Form
from datetime import datetime


def transactions_queries(request, get_accounts, set_query, fetch_query):
    if request.method == 'POST':
        # OBTENER CUENTAS
        username = request.session['auth']['username']
        account_res = get_accounts(request)

        # CREAR FORMULARIO NUEVO
        form = Transactions_Form(data=request.POST)
        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data
            amount = data.get('amount')
            description = data.get('description')
            originAccount = request.POST['originAccount']
            destAccount = request.POST['destAccount']

            # FECHA ACTUAL
            now = datetime.now()
            date = now.strftime("%Y/%m/%d")

            # LEER ÚNICA CUENTA
            current_account = None
            for account in account_res:
                if str(account['id']) == str(originAccount):
                    current_account = account

            # VERIFICAR QUE NO SEA LA MISMA CUENTA
            if originAccount != destAccount:
                # LEER CUENTA DE TERCEROS
                dest_account = fetch_query(
                    f'SELECT * FROM Account WHERE id = {destAccount}')

                # BUSCAR CUENTA DE DESTINO
                if dest_account[0]:

                    # VERIFICAR SI TIENE EL SALDO
                    if float(current_account['balance']) >= float(amount):
                        # CREAR TRANSACCION
                        set_query(
                            f'INSERT INTO Transactions VALUES (null, {amount}, "{description}", "{date}", {originAccount}, {destAccount}, 0)')

                        # AGREGAR DEBITO A CUENTA
                        total_amount = float(amount)
                        if str(dest_account[0][6]) == '1' and str(current_account['isDollar']) == '0':
                            total_amount = float(amount) / 7.87
                        elif str(dest_account[0][6]) == '0' and str(current_account['isDollar']) == '1':
                            total_amount = float(amount) * 7.60

                        # AGREGAR DEBITO A CUENTA PROPIA
                        set_query(
                            f'UPDATE Account SET debit = debit + {float(amount)} WHERE id = {originAccount}')

                        # AGREGAR CREDITO A OTRA CUENTA
                        set_query(
                            f'UPDATE Account SET credit = credit + {total_amount} WHERE id = {destAccount}')
