from ..forms import Loans_Form

# CALCULAR INTERÉS


def compute_interest(req_plan, req_amount):
    interest = 0.05

    if req_amount >= 1000 and req_amount <= 5000:
        if req_plan == 12:
            interest = 0.05
        elif req_plan == 24:
            interest = 0.04
        elif req_plan == 36:
            interest = 0.0335
        elif req_plan == 48:
            interest = 0.025
    elif req_amount >= 5000.01 and req_amount <= 15000:
        if req_plan == 12:
            interest = 0.0525
        elif req_plan == 24:
            interest = 0.0415
        elif req_plan == 36:
            interest = 0.0350
        elif req_plan == 48:
            interest = 0.026
    elif req_amount >= 15000.01 and req_amount <= 30000:
        if req_plan == 12:
            interest = 0.053
        elif req_plan == 24:
            interest = 0.042
        elif req_plan == 36:
            interest = 0.0355
        elif req_plan == 48:
            interest = 0.0265
    elif req_amount >= 30000.01 and req_amount <= 60000:
        if req_plan == 12:
            interest = 0.0535
        elif req_plan == 24:
            interest = 0.0425
        elif req_plan == 36:
            interest = 0.036
        elif req_plan == 48:
            interest = 0.027
    elif req_amount >= 60000.01:
        if req_plan == 12:
            interest = 0.0545
        elif req_plan == 24:
            interest = 0.0435
        elif req_plan == 36:
            interest = 0.037
        elif req_plan == 48:
            interest = 0.028
    return interest


def loans_queries(request, set_query, fetch_query, render, user):
    if request.method == "POST":
        # FORMULARIO
        form = Loans_Form(data=request.POST)

        # USUARIO
        userCui = user.get('cui', "")
        userBusiness = user.get('comercialName', "")
        userBusiness = f'"{userBusiness}"' if len(
            userBusiness) > 0 else "null"
        userCui = userCui if len(str(userCui)) > 0 else "null"

        if form.is_valid():
            data = form.cleaned_data

            # VARIABLES
            amount = data.get('amount', 0)
            description = data.get('description', '')
            plan = request.POST.get('plan', '12')
            isRequest = request.POST.get('isRequest', '0').replace('on', '1')
            isRequest = isRequest == '1'

            # COTIZAR
            interest = compute_interest(int(plan), float(amount))
            if not isRequest:
                quota = float(amount) / int(plan)

                # COTIZAR
                quotas = {
                    "pays": str(plan) + " pagos",
                    "withInterest": quota + (quota * interest),
                    "withoutInterest": quota
                }

                # NUEVAS VARIABLES
                return {
                    "form": render['form'],
                    "accounts": render['accounts'],
                    "loans": render['loans'],
                    "user": render['user'],
                    "quotas": quotas,
                }

            # SOLICITAR
            else:
                set_query(
                    f'INSERT INTO Loans VALUES (null, {amount}, {plan}, {interest}, "{description}", 0, 0, {userCui}, {userBusiness})')
                return render
        else:
            return render


def loan_quotas_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        data = request.POST

        # VARIABLES
        account_id = data.get('account', '-1')
        quota_id = data.get('quota', '-1')
        payDate = data.get('payDate', '').replace('-', '/')

        # QUOTA
        quota = fetch_query(f'SELECT * FROM LoanQuotas WHERE id = {quota_id}')
        account = fetch_query(f'SELECT * FROM Account WHERE id = {account_id}')

        if quota and quota[0]:
            # PRESTAMO
            loan = fetch_query(f'SELECT * FROM Loans WHERE id = {quota[0][1]}')

            if loan and loan[0]:
                if account and account[0]:
                    # CALCULAR CONVERSION Q - $
                    isDollar = str(account[0][6]) == '1'
                    balance = float(
                        account[0][4]) * 7.87 if isDollar else float(account[0][4])
                    loan_quota = float(quota[0][4])

                    if balance >= loan_quota:
                        # INTERÉS
                        interest = compute_interest(
                            int(loan[0][2]), float(loan[0][1]))
                        new_quota = loan_quota + (loan_quota * interest)

                        # CALCULAR CONVERSION Q - $
                        if isDollar:
                            new_quota = new_quota / 7.87
                            loan_quota = loan_quota / 7.87

                        # QUOTA
                        quota_year = int(
                            quota[0][2].strftime("%Y/%m/%d")[0:-6])
                        quota_month = int(
                            quota[0][2].strftime("%Y/%m/%d")[5:-3])
                        year = int(payDate[0:-6])
                        month = int(payDate[5:-3])

                        # CON INTERÉS
                        if quota_year == year and month >= quota_month:
                            # PAGAR CUOTA
                            set_query(
                                f'UPDATE LoanQuotas SET payDate = "{payDate}", account = {account_id} WHERE id = {quota_id}')

                            set_query(
                                f'UPDATE Account SET debit = debit + {new_quota} WHERE id = {account_id}'
                            )

                        # SIN INTERÉS
                        if quota_year >= year and quota_month > month:
                            # PAGAR CUOTA
                            set_query(
                                f'UPDATE LoanQuotas SET payDate = "{payDate}", account = {account_id} WHERE id = {quota_id}')

                            set_query(
                                f'UPDATE Account SET debit = debit + {loan_quota} WHERE id = {account_id}'
                            )
