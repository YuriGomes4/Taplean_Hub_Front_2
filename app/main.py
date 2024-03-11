from datetime import datetime, timedelta
import difflib
import json
from flask import Flask, redirect, render_template, request, url_for
import functools
from flask_cors import CORS
import requests

import services
import pandas as pd
import plotly.express as px

app = Flask(__name__)

CORS(app)

base_url = services.config.get('url_base')

def token_required(route_func):
    @functools.wraps(route_func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if token:
            response = requests.get(f'{base_url}/api/auth/verify', headers={'x-access-token': token})
            if response.status_code == 200:
                return route_func(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
@token_required
def index():
    return redirect(url_for('graficos'))
	
@app.route("/login")
#@token_required
def login():
    token = request.cookies.get('token')
    if token:
        response = requests.get(f'{base_url}/api/auth/verify', headers={'x-access-token': token})
        if response.status_code == 200:
            return redirect(url_for('graficos'))
        else:
            pagina = "login"
            return render_template("login.html", base_url=base_url, pagina=pagina)
    else:
        pagina = "login"
        return render_template("login.html", base_url=base_url, pagina=pagina)

@app.route("/graficos")
@token_required
def graficos():
    pagina = "graficos"

    estados_brasil = {
        "Brasil": "BR",
        "Acre": "AC",
        "Alagoas": "AL",
        "Amapá": "AP",
        "Amazonas": "AM",
        "Bahia": "BA",
        "Ceará": "CE",
        "Distrito Federal": "DF",
        "Espírito Santo": "ES",
        "Goiás": "GO",
        "Maranhão": "MA",
        "Mato Grosso": "MT",
        "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG",
        "Pará": "PA",
        "Paraíba": "PB",
        "Paraná": "PR",
        "Pernambuco": "PE",
        "Piauí": "PI",
        "Rio de Janeiro": "RJ",
        "Rio Grande do Norte": "RN",
        "Rio Grande do Sul": "RS",
        "Rondônia": "RO",
        "Roraima": "RR",
        "Santa Catarina": "SC",
        "São Paulo": "SP",
        "Sergipe": "SE",
        "Tocantins": "TO"
    }

    return render_template("principais/graficos.html", base_url=base_url, pagina=pagina, estados_brasil=estados_brasil)

@app.route("/produtos")
@token_required
def produtos():
    pagina = "produtos"
    return render_template("principais/produtos.html", base_url=base_url, pagina=pagina)

@app.route("/produto/<string:mlb>")
@token_required
def produto(mlb):
    pagina = "produtos"
    return render_template("principais/produto.html", base_url=base_url, pagina=pagina, mlb=mlb)

@app.route("/anuncios")
@token_required
def anuncios():
    pagina = "anuncios"
    return render_template("principais/anuncios.html", base_url=base_url, pagina=pagina)

@app.route("/anuncios/pesquisar")
@token_required
def anuncios_pesquisar():
    pagina = "anuncios"
    return render_template("principais/anuncios_pesquisar.html", base_url=base_url, pagina=pagina)

@app.route("/analise_mercado")
@token_required
def analise_mercado():
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado.html", base_url=base_url, pagina=pagina)

@app.route("/analise_mercado/nova")
@token_required
def nova_analise_mercado():
    pagina = "analise_mercado"
    return render_template("principais/nova_analise_mercado.html", base_url=base_url, pagina=pagina)

@app.route("/analise_mercado/<string:id_pesquisa>")
@token_required
def ver_analise_mercado(id_pesquisa):
    pagina = "analise_mercado"
    return render_template("principais/ver_analise_mercado.html", base_url=base_url, pagina=pagina, id_pesquisa=id_pesquisa)

@app.route("/analise_mercado/<string:id_pesquisa>/addprodutos")
@token_required
def analise_mercado_addprodutos(id_pesquisa):
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado_addprodutos.html", base_url=base_url, pagina=pagina, id_pesquisa=id_pesquisa)

@app.route("/conta")
@token_required
def conta():
    pagina = "conta"
    return render_template("principais/conta.html", base_url=base_url, pagina=pagina)

@app.route("/administracao")
@token_required
def administracao():
    pagina = "administracao"
    return render_template("principais/administracao.html", base_url=base_url, pagina=pagina)

app.static_folder = 'templates/assets'

if __name__ == "__main__":
    app.run(port=5050, debug=True, host="0.0.0.0")
