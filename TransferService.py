import ExchangeRateService as ERS

INTEREST_RATE = 0.1


def currency_to_czk(amount, currency):
    """Převod částky 'amount' z 'currency' na CZK podle 'exchange_rates'."""
    exchange_rates = ERS.get_exchange_rates()
    return round((amount * exchange_rates[currency]), 2)


def process_payment(user, amount, currency):
    if amount > 0:
        payment_incoming(user, amount, currency)
    else:
        payment_outgoing(user, -amount, currency)


def payment_incoming(user, amount, currency):
    if currency not in user.account:
        amount = currency_to_czk(amount, currency)
        currency = 'CZK'
    user.account[currency] += amount


def payment_outgoing(user, amount, currency):
    done = False
    if currency in user.account.keys():
        if user.account.get(currency, 0) >= amount:
            payment_incoming(user, -amount, currency)
            done = True
        else:
            done = payment_outgoing_credit(user, amount, currency)

    if not done:
        if user.account.get('CZK', 0) >= (tmp := currency_to_czk(amount, currency)):
            payment_incoming(user, -tmp, 'CZK')
            done = True
        else:
            done = payment_outgoing_credit(user, tmp, 'CZK')

    return done


def payment_outgoing_credit(user, amount, currency):
    balance = user.account.get(currency, 0)
    if balance * (1 + INTEREST_RATE) >= amount:
        missing = balance - amount
        missing_with_interest = missing * (1 + INTEREST_RATE)
        total = round(float((missing_with_interest - balance)), 2)
        payment_incoming(user, total, currency)
        return True
    return False
