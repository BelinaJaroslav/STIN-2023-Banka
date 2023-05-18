import ExchangeRateService as ERS


def currency_to_czk(amount, currency):
    """Převod částky 'amount' z 'currency' na CZK podle 'exchange_rates'."""
    exchange_rates = ERS.get_exchange_rates()
    return round((amount * exchange_rates[currency]), 2)


def process_payment(user, amount, currency):
    if amount > 0:
        payment_incoming(user, amount,currency)
    else:
        payment_outgoing(user, -amount, currency)


def payment_incoming(user, amount,currency):
    if currency not in user.account:
        amount = currency_to_czk(amount,currency)
        currency = 'CZK'
    user.account[currency]+=amount


def payment_outgoing(user, amount, currency):
    if user.account.get(currency, 0) >= amount:
        payment_incoming(user, -amount, currency)
    elif currency != 'CZK' and user.account.get('CZK', 0) >= (tmp := currency_to_czk(amount, currency)):
        payment_incoming(user, -tmp, 'CZK')
