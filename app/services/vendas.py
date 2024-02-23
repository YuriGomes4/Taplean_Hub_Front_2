#from . import personal_prefs
import requests
from flask import request

from services import config


def get_all(seller_id, date_from=None, date_to=None):
    url_base = config.get('url_base')  # http://127.0.0.1:5000

    headers = {
        'x-access-token' : request.cookies.get('token'),
    }

    update_url = f"{url_base}/api/v1/vendas/all"

    params = {
        "seller_id": seller_id,
    }

    if date_from and date_to:
        params["date_from"] = date_from,
        params["date_to"] = date_to,
        response = requests.get(update_url, headers=headers, params=params)
    else:
        response = requests.get(update_url, headers=headers, params=params)

    if response.status_code == 200:
        print("Vendas listadas com sucesso!")
        return response.json()['result']
    else:
        print("Falha ao listar as vendas.")
        print(response.json())

def ver_vendas_intervalo(seller, dias, termino):
    url_base = config.get('url_base')  # http://127.0.0.1:5000

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-access-token' : request.cookies.get('token'),
    }

    params = {
        'last': dias,
        'ending': termino
    }

    update_url = f"{url_base}/api/v1/vendas/{seller}/time_window"

    response = requests.get(update_url, headers=headers, params=params)

    if response.status_code == 200:
        print("Vendas listadas com sucesso!")
        return response.json()['result']
    else:
        print("Falha ao listar as vendas do item.")
        return None