def login_form(request, get_query):
    if request.method == 'POST':
        # VARIABLES
        username = request.POST['username']
        password = request.POST['password']

        # VERIFICAR
        cursor = get_query(
            f'SELECT * FROM SingleUser WHERE username = "{username}" AND password = "{password}";')
        cursor[0].commit()

        # LISTA
        user = cursor[1].fetchall()

        # CERRAR
        cursor[1].close()

        if len(user) > 0:
            return True
        else:
            return False
