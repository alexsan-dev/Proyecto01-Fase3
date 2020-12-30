from datetime import date, datetime
import calendar

# AGREGAR MES


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


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
            loan_quota = float(current_loan[0][1])/int(current_loan[0][2])

            for x in range(int(current_loan[0][2])):
                # SIGUIENTE MES
                next_month = add_months(now, 1)
                now = next_month

                # INSERT
                set_query(
                    f'INSERT INTO LoanQuotas VALUES (null, {loan},"{next_month.strftime("%Y/%m/%d")}",null,{loan_quota},null)')
