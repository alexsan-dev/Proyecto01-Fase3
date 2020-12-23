def login_queries(request, fetch_query):
    if request.method == 'POST':
        # VARIABLES
        username = request.POST['username']
        password = request.POST['password']

        # VERIFICAR
        user = fetch_query(
            f'SELECT * FROM SingleUser WHERE username = "{username}" AND password = "{password}";')
        business_user = fetch_query(
            f'SELECT * FROM BusinessUser WHERE comercialName = "{username}" AND password = "{password}";')

        if len(user) > 0 or len(business_user) > 0:
            return True
        else:
            return False
