from datetime import date, datetime
import calendar

# AGREGAR MES


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

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


def loans_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        # VARIABLES
        data = request.POST
        loan = data.get('loan', '')

        # UPDATE
        set_query(f'UPDATE Loans SET authorized = 1 WHERE id = {loan}')
        current_loan = fetch_query(f'SELECT * FROM Loans WHERE id = {loan}')

        # FECHA ACTUAL
        now = date.today()

        # INSERT QUOTAS
        if current_loan and current_loan[0]:
            # CUOTAS
            quota = float(current_loan[0][1])/int(current_loan[0][2])
            quota += quota * compute_interest(int(current_loan[0][2]), quota)

            for x in range(int(current_loan[0][2])):
                # SIGUIENTE MES
                next_month = add_months(now, 1)
                now = next_month

                # INSERT
                set_query(
                    f'INSERT INTO LoanQuotas VALUES (null, {loan},"{next_month.strftime("%Y/%m/%d")}",null,{quota},null)')
