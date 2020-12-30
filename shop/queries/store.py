from ..forms import *


def compute_points(req_amount, brand):
    points = 0

    if brand == 'Prefepuntos':
        if req_amount >= 0.01 and req_amount <= 100:
            points = 0
        elif req_amount >= 100.01 and req_amount <= 500:
            points = 0.02
        elif req_amount >= 500.01 and req_amount <= 2000:
            points = 0.04
        elif req_amount >= 2000.01:
            points = 0.05
    elif brand == 'Cashback':
        if req_amount >= 0.01 and req_amount <= 200:
            points = 0
        elif req_amount >= 200.01 and req_amount <= 700:
            points = 0.02
        elif req_amount >= 700.01:
            points = 0.05

    return points


def store_queries(request, set_query, fetch_query):
    if request.method == 'POST':
        # FORMULARIO
        form = Purchases_Form(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # VARIABLES
            amount = data.get('amount', 0)
            description = data.get('description', '')
            isDollar = data.get('isdollar')
            date = request.POST.get('date', '').replace('-', '/')
            card = request.POST.get('card', '')

            # QUERIES
            current_card = fetch_query(
                f'SELECT * FROM Cards WHERE id = {card}')

            # TARJETA
            if current_card and current_card[0]:
                card_brand = current_card[0][1]

                # CONVERTIR SALDO A QUETZAL
                badge = 7.63 if card_brand == 'Prefepuntos' else 7.87
                purchase_amount = float(
                    amount) * badge if isDollar else float(amount)
                card_balance = float(
                    current_card[0][2]) - float(current_card[0][3])
                points = compute_points(purchase_amount, card_brand)

                # VALIDAR SALDO
                if card_balance >= purchase_amount:
                    prefepoints = purchase_amount * points if card_brand == 'Prefepuntos' else 0
                    cashback = purchase_amount * points if card_brand == 'Cashback' else 0

                    # FETCH
                    purchases = fetch_query(f'SELECT * FROM Purchases')
                    next_purchase = len(purchases)

                    # INSERT
                    set_query(
                        f'INSERT INTO Purchases VALUES (null, "{date}", "{description}", {purchase_amount}, {"1" if isDollar else "0"}, {card})')
                    set_query(
                        f'INSERT INTO CardTransaction VALUES (null, {next_purchase + 1} ,{prefepoints}, {cashback})'
                    )

                    # UPDATE
                    set_query(
                        f'UPDATE Cards SET debit = debit + {purchase_amount}, credit = credit + {cashback} WHERE id = {card}')
