from ..forms import Spreads_Form


def spreads_queries(request, user, set_query, fetch_query, accounts):
    if request.method == 'POST':
        # FORMULARIO
        form = Spreads_Form(data=request.POST)

        def insert_pay(req_account, isMensualPayPlan, amount, employAccount, employName):
            # NOMBRE DE EMPRESA
            userBusiness = user.get('comercialName', '')

            # CUENTA
            current_account = None
            for user_account in accounts:
                if user_account['id'] == req_account:
                    current_account = user_account

            # SELECCIONAR PAGO
            prevPay = fetch_query(
                f'SELECT * FROM SpreadsPay WHERE employAccount = {employAccount}')

            if current_account:
                if float(str(current_account['balance'])) >= float(str(amount)):
                    # DEBIT DE LA CUENTA
                    def debit_from():
                        set_query(
                            f'UPDATE Account SET debit = debit + {amount} WHERE id = {req_account}')

                    if prevPay and prevPay[0]:
                        # UPDATE
                        set_query(
                            f'UPDATE SpreadsPay SET amount = {amount}, isMensualPayPlan = {isMensualPayPlan} WHERE employAccount = {employAccount}')
                        debit_from()

                    else:
                        # INSERT
                        set_query(
                            f'INSERT INTO SpreadsPay VALUES (null, {employAccount}, "{employName}", {amount}, {isMensualPayPlan}, "{userBusiness}", {req_account})')
                        debit_from()

        # ARCHIVO
        file = request.FILES.get('csv', None)
        csv = []

        if file:
            # MATRIZ
            csv = str(file.read())[2:][:-1].split('\\n')
            col_counter = 0

            for row in csv:
                # COLUMNAS
                cols = row.split(',')

                if col_counter > 0:
                    file_account = cols[0]
                    file_amount = cols[1]
                    file_mensual = cols[2]
                    file_empAccount = cols[3]
                    file_empName = cols[4]

                    # ACTUALIZAR
                    insert_pay(file_account, file_mensual, file_amount,
                               file_empAccount, file_empName)

                col_counter += 1

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            account = request.POST.get('account', '')
            isMensualPayPlan = data.get('ismensualpayplan', False)
            isMensualPayPlan = '1' if isMensualPayPlan else '0'
            amount = data.get('amount', 0)
            employAccount = data.get('employaccount', '')
            employName = data.get('employname', '')

            # PAGAR
            insert_pay(account, isMensualPayPlan, amount,
                       employAccount, employName)
