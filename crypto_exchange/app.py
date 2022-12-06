import argparse
import requests


def parser():
    parser = argparse.ArgumentParser(description='Exchange crypto currency to a given currency')

    parser.add_argument('amount', type=float,
                        help='a float number for the crypto currency')
    parser.add_argument('crypto_currency', type=str,
                        help="crypto currncy's name")
    parser.add_argument('currency', type=str,
                        help="currency's name")
    args = parser.parse_args()
    return args


data = parser()


def fetch_symbol(crypto: str) -> str:
    r = requests.get('https://api.coingecko.com/api/v3/coins/list')
    symbols = r.json()

    for i in range(len(symbols)):
        if symbols[i]['id'] == crypto:
            return symbols[i]['symbol']


def fetch_rates(crypto: str, currency: str) -> float:
    r = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}")

    rate = r.json()

    for i in range(len(rate)):
        if rate[i]['id'] == crypto:
            return rate[i]['current_price']


def conversion(amount: float, crypto_currency: str, normal_currency: str) -> float:
    exchange_rate = fetch_rates(crypto_currency, normal_currency)
    return round(amount * exchange_rate, 2)


input = (data.amount, data.crypto_currency, data.currency)
output = conversion(amount=input[0], crypto_currency=input[1], normal_currency=input[2])

print(f"{fetch_symbol(data.crypto_currency)} {data.amount} = USD {output}")
