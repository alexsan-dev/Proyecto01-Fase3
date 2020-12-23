def checks_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        # VARIABLES
        check_account = request.POST.get('check_account', '')
        check_enable = request.POST.get('check_enable', '0').replace('on', '1')
        account = request.POST.get('account', '')
        check = request.POST.get('check', '')

        # OBTENER CHEQUE
        account_check = None
        if len(str(account)) > 0 and len(str(check)) > 0:
            account_check = fetch_query(
                f'SELECT * FROM AccountCheck WHERE account = {account} AND id = {check}')

        enable_check = None
        if len(str(check_account)) > 0 and len(str(check_enable)) > 0:
            enable_check = fetch_query(
                f'SELECT * FROM Account WHERE id = {check_account}'
            )

        if account_check and account_check[0]:
            # QUERY
            set_query(f'INSERT INTO AuthCheck VALUES ({check[0][0]}, 1)')

        if enable_check and enable_check[0]:
            # QUERY
            set_query(
                f'UPDATE Account SET enableChecks = {check_enable} WHERE id = {check_account}')
