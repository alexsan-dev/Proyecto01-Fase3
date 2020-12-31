def cards_queries(request, fetch_query, render):
    if request.method == 'POST':
        card_id = request.POST.get('card', '')
        cards = fetch_query(f'SELECT * FROM Cards WHERE id = {card_id}')
        purchases = fetch_query(
            f'SELECT * FROM Purchases RIGHT JOIN CardTransaction on Purchases.id WHERE idCard = {card_id}')

        if cards[0]:
            render = {
                "cards": render['cards'],
                "cardsData": cards[0],
                "purchases": purchases
            }
            return render
        else:
            return render
