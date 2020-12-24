def deposits_queries(request, set_query):
    if request.method == 'POST':
        # VARIABLES
        data = request.POST
        account = data.get('account', '')
        credit = data.get('credit', 0) or 0
        debit = data.get('debit', 0) or 0

        # QUERIES
        set_query(
            f'UPDATE Account SET credit = credit + {credit}, debit = debit + {debit} WHERE id = {account}')
