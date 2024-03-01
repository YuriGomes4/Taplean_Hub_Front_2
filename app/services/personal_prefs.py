#import streamlit as st
import json
import requests
from . import config
from flask import request

def get_all():
    return json.loads(str(request.cookies.get('prefs')).replace("'", '"'))

def get(name):
    data = json.loads(str(request.cookies.get('prefs')).replace("'", '"'))

    try:
        return data[name]
    except:
        from . import default_prefs

        try:
            set(name, default_prefs.get(name))
        except:
            pass

def set(name, value):
    try:
        json.loads(str(request.cookies.get('prefs')).replace("'", '"'))[name] = value

        url_base = config.get("url_base")

        update_url = f"{url_base}/api/v1/usuario/preferences"

        headers = {
            'x-access-token' : str(request.cookies.get('token')),
        }

        params = {
            'dados': str(json.loads(str(request.cookies.get('prefs')).replace("'", '"')))
        }

        response = requests.put(update_url, headers=headers, params=params)
    except:
        pass
    return get(name)

#for key, value in get_all().items():
#    print(f'{key}: {value}')

