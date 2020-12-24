from ..forms import ThirdAccount_Form


def accounts_queries(request, fetch_query, set_query, user):
    if request.method == 'POST':
        # FORMULARIO
        form = ThirdAccount_Form(data=request.POST)

        if form.is_valid():
            # LEER FORMULARIO
            data = form.cleaned_data

            # VARIABLES
            account_id = data.get('id')
            userCui = user.get('cui', "")
            userBusiness = user.get('comercialName', "")
            account_type = request.POST.get('account_type', '')

            # LEER CUENTAS CON ESE ID
            third_account = fetch_query(
                f'SELECT * FROM Account LEFT JOIN AccountType ON Account.id = AccountType.id WHERE Account.id = {account_id}')

            # VERIFICAR QUE NO ES UNA CUENTA PROPIA
            if third_account[0]:
                if third_account[0][7] != userCui and third_account[0][8] != userBusiness:
                    valid_type = False

                    # VERIFICAR EL TIPO DE CUENTA
                    if account_type == 'Ahorro' and third_account[0][12] == account_id:
                        valid_type = True

                    elif account_type == 'Plazo fijo' and third_account[0][13] == account_id:
                        valid_type = True

                    elif third_account[0][14] == account_id:
                        valid_type = True

                    if valid_type:
                        # CONVERTIR NULLS
                        third_userCui = third_account[0][7] if third_account[0][7] else "null"
                        third_userBusiness = f'"{third_account[0][8]}"' if third_account[0][8] else "null"
                        userBusiness = f'"{userBusiness}"' if len(
                            userBusiness) > 0 else "null"
                        userCui = userCui if len(str(userCui)) > 0 else "null"

                        # INSERTAR CUENTA DE TERCEROS

                        set_query(
                            f'INSERT INTO ThirdAccount VALUES ({account_id}, {userCui}, {userBusiness}, {third_userCui}, {third_userBusiness}, "{account_type}"); ')
