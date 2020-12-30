from ..forms import Loans_Form


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

        # CALCULAR INTERÉS
        def compute_interest(req_plan, req_amount):
            interest = 0.05

            if req_amount >= 1000 and req_amount <= 5000:
                if plan == 12:
                    interest = 0.05
                elif plan == 24:
                    interest = 0.04
                elif plan == 36:
                    interest = 0.0335
                elif plan == 48:
                    interest = 0.025
            elif req_amount >= 5000.01 and req_amount <= 15000:
                if plan == 12:
                    interest = 0.0525
                elif plan == 24:
                    interest = 0.0415
                elif plan == 36:
                    interest = 0.0350
                elif plan == 48:
                    interest = 0.026
            elif req_amount >= 15000.01 and req_amount <= 30000:
                if plan == 12:
                    interest = 0.053
                elif plan == 24:
                    interest = 0.042
                elif plan == 36:
                    interest = 0.0355
                elif plan == 48:
                    interest = 0.0265
            elif req_amount >= 30000.01 and req_amount <= 60000:
                if plan == 12:
                    interest = 0.0535
                elif plan == 24:
                    interest = 0.0425
                elif plan == 36:
                    interest = 0.036
                elif plan == 48:
                    interest = 0.027
            elif req_amount >= 60000.01:
                if plan == 12:
                    interest = 0.0545
                elif plan == 24:
                    interest = 0.0435
                elif plan == 36:
                    interest = 0.037
                elif plan == 48:
                    interest = 0.028
            return interest

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
                    "quotas": quotas
                }

            # SOLICITAR
            else:
                set_query(
                    f'INSERT INTO Loans VALUES (null, {amount}, {plan}, {interest}, "{description}",0, 0, {userCui}, {userBusiness})')
                return render
