from datetime import datetime, timedelta
from decimal import Decimal
import requests
import csv

date_cache = None
exchange_rates = None
update_date = None
url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"


def get_exchange_rates():
    global exchange_rates

    load_exchange_rates()
    return exchange_rates


def load_exchange_rates():
    global exchange_rates
    global update_date

    if not exchange_rates:
        download_actual_exchange_rates()
    elif datetime.now() > update_date:
        download_actual_exchange_rates()


def download_actual_exchange_rates():
    global exchange_rates
    global update_date
    try:
        response = requests.get(url, timeout=10).text
        exchange_rates = parse_exchange_rates(response)
        now = datetime.today()
        update_date = datetime(now.year, now.month, now.day, 14, 30, 0) + timedelta(days=1)
        while not update_date.weekday() < 5:
            update_date += timedelta(days=1)
    except:
        return None


def parse_exchange_rates(response):
    exchange_rates_loc = {
        code: float(rate) / float(amt)
        for _, _, amt, code, rate in csv.reader(response.replace(',', '.').splitlines()[2:], delimiter='|')
    }
    return exchange_rates_loc
