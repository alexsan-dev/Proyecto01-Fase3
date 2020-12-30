from ..forms import Spreads_Form


def spreads_queries(request, user, set_query, fetch_query):
    if request.method == 'POST':
        # FORMULARIO
        form = Spreads_Form(data=request.POST)
        account = request.POST.get('account', '')

        def insert_pay(req_account, isMensualPayPlan, amount, payAccount, payName):
            # NOMBRE DE EMPRESA
            userBusiness = user.get('comercialName', '')
            isProvider = request.POST.get('isProvider', '0').replace('on', '1')
            isProvider = isProvider == '1'

            # NOMBRE DE TABLA
            tableName = "ProvidersPay" if isProvider else "SpreadsPay"

            # CUENTA
            current_account = fetch_query(
                f'SELECT * FROM Account WHERE id = {req_account}')

            # SELECCIONAR PAGO
            prevPay = fetch_query(
                f'SELECT * FROM {tableName} WHERE payAccount = {payAccount}')
            pay_account = fetch_query(
                f'SELECT * FROM Account WHERE id = {payAccount}')

            if current_account and current_account[0] and len(pay_account) > 0:
                current_account_balance = float(
                    current_account[0][4]) - float(current_account[0][5])

                if current_account_balance >= float(str(amount)):
                    # DEBIT DE LA CUENTA
                    def debit_from():
                        set_query(
                            f'UPDATE Account SET debit = debit + {amount} WHERE id = {req_account}')

                    if prevPay and prevPay[0]:
                        # UPDATE
                        set_query(
                            f'UPDATE {tableName} SET amount = {amount}, isMensualPayPlan = {isMensualPayPlan} WHERE payAccount = {payAccount}')
                        debit_from()

                    else:
                        # INSERT
                        set_query(
                            f'INSERT INTO {tableName} VALUES (null, {payAccount}, "{payName}", {amount}, {isMensualPayPlan}, "{userBusiness}", {req_account})')
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
                    file_payName = cols[0]
                    file_payAccount = cols[1]
                    file_amount = cols[2]

                    # ACTUALIZAR
                    insert_pay(account, 1, file_amount,
                               file_payAccount, file_payName)

                col_counter += 1

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            isMensualPayPlan = data.get('ismensualpayplan', False)
            isMensualPayPlan = '1' if isMensualPayPlan else '0'
            amount = data.get('amount', 0)
            payAccount = data.get('payaccount', '')
            payName = data.get('payname', '')

            # PAGAR
            insert_pay(account, isMensualPayPlan, amount,
                       payAccount, payName)
