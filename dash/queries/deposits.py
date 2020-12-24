def deposits_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        # VARIABLES
        data = request.POST

        # RECUPERAR
        account = data.get('account', '')
        debit_type = data.get('debit_type', 'Quetzal')
        credit_type = data.get('credit_type', 'Quetzal')
        credit = data.get('credit', 0) or 0
        debit = data.get('debit', 0) or 0

        # CUENTA
        current_account = fetch_query(
            f'SELECT isDollar FROM Account WHERE id = {account}')

        # TAZA
        if current_account and current_account[0]:
            # CALCULAR CREDITO
            total_credit = credit
            if credit_type == 'Quetzal' and current_account[0][0] == 1:
                total_credit = float(total_credit) / 7.87
            elif credit_type == 'Dollar' and current_account[0][0] == 0:
                total_credit = float(total_credit) * 7.6

            # CALCULAR DEBITO
            total_debit = debit
            if debit_type == 'Quetzal' and current_account[0][0] == 1:
                total_debit = float(total_debit) / 7.87
            elif debit_type == 'Dollar' and current_account[0][0] == 0:
                total_debit = float(total_debit) * 7.6

            # QUERIES
            set_query(
                f'UPDATE Account SET credit = credit + {total_credit}, debit = debit + {total_debit} WHERE id = {account}')
