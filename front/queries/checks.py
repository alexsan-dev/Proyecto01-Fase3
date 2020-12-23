def checks_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        # VARIABLES
        account = request.POST.get('account')
        check = request.POST.get('check')

        # OBTENER CHEQUE
        check = fetch_query(
            f'SELECT * FROM AccountCheck WHERE account = {account} AND id = {check}')

        if check[0]:
            # QUERY
            set_query(f'INSERT INTO AuthCheck VALUES ({check[0][0]}, 1)')
