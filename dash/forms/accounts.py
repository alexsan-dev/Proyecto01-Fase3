def accounts_form(request, set_query):
    if request.method == 'POST':
        # VARIABLES
        userCui = request.POST['userCui']
        userCui = 'null' if len(userCui) == 0 else userCui

        # NOMBRE COMERCIAL
        userBusiness = request.POST['userBusiness']
        userBusiness = 'null' if len(
            userBusiness) == 0 else '"'+userBusiness+'"'

        # INFORMACIÓN DE LA CUENTA
        accountId = request.POST['accountId']
        isSingle = request.POST.get('isSingle', '0').replace('on', '1')
        isDollar = request.POST.get('isDollar', '0').replace('on', '1')
        accountType = request.POST['accountType']
        interest = request.POST['interest']
        description = request.POST['description']
        plan = request.POST['plan'].replace('-', '/')

        # INSERTAR EN TIPO DE CUENTA
        if accountType == 'saving':
            set_query(
                f'INSERT INTO SavingAccount VALUES ({accountId}, {interest}); ')
            set_query(
                f'INSERT INTO AccountType(id, saving) VALUES ({accountId}, {accountId}); ')
        elif accountType == 'timedSaving':
            set_query(
                f'INSERT INTO TimedSavingAccount VALUES ({accountId}, {interest}, {plan}); ')
            set_query(
                f'INSERT INTO AccountType(id, timedSaving) VALUES ({accountId}, {accountId}); ')
        elif accountType == 'monetary':
            set_query(
                f'INSERT INTO MonetaryAccount VALUES ({accountId}, "{description}"); ')
            set_query(
                f'INSERT INTO AccountType(id, monetary) VALUES ({accountId}, {accountId}); ')

        # INSERTAR EN CUENTA
        set_query(
            f'INSERT INTO Account VALUES ({accountId}, 1, 0, {isSingle}, 0, 0, {isDollar}, {userCui}, {userBusiness}); ')
