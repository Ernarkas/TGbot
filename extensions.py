import json

import requests

from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена🥺")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            return APIException(f"Валюта {sym} не найдена🥺")

        if base_key == sym_key:
            raise APIException(f"Невозможно конвертировать одинаковые валюты {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://api.exchangerate.host/convert?from={base_key}&to={sym_key}")
        resp = json.loads(r.content)
        converted_amount = amount * resp['info']['rate']
        converted_amount = round(converted_amount, 2)
        message = f"{amount} {base} эквивале́нто {converted_amount:.2f} {sym}"
        return message



