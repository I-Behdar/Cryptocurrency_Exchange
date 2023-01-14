import argparse
import requests


def parser():
    parser = argparse.ArgumentParser(description='Exchange crypto currency to a given currency')

    parser.add_argument('amount', type=float,
                        help='a float number for the crypto currency')
    parser.add_argument('crypto_currency', type=str,
                        help="crypto currency's name")
    parser.add_argument('currency', type=str,
                        help="currency's name")
    args = parser.parse_args()
    return args


def fetch_crypto_symbol(crypto: str) -> str:
    r = requests.get('https://api.coingecko.com/api/v3/coins/list')
    symbols = r.json()
    try:
        for i in range(len(symbols)):
            if symbols[i]['id'] == crypto:
                return symbols[i]['symbol']
    except KeyError:
        return (f"(No Symbol)")

def fetch_rates(crypto: str, currency: str) -> float:
    r = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}")

    rate = r.json()
    try:
        for i in range(len(rate)):
            if rate[i]['id'] == crypto:
                return rate[i]['current_price']
    except KeyError:
        return 0


def conversion(amount: float, crypto_currency: str, normal_currency: str) -> float:
    exchange_rate = fetch_rates(crypto_currency, normal_currency)
    return round(amount * exchange_rate, 2)


if __name__ == '__main__':
    args = parser()
    output = conversion(amount=args.amount, crypto_currency=args.crypto_currency, normal_currency=args.currency)
    if output != 0:
        print(f"{fetch_crypto_symbol(args.crypto_currency)} {args.amount} = {args.currency} {output}")
    print("Data currently not available!")
