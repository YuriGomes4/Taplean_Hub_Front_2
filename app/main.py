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
    pagina = "login"
    return render_template("login.html", base_url=base_url, pagina=pagina)

@app.route("/graficos")
@token_required
def graficos():
    pagina = "graficos"

    semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_da_semana = []

    for i in range(7):
        # Calcule a data do dia atual na sequência.
        data_dia_atual = (datetime.today() - timedelta(days=6)) + timedelta(days=i)
        
        # Obtenha o nome do dia da semana para a data atual.
        dia_da_semana.append(semana[data_dia_atual.weekday()])
        
        #print(f"No {nome_dia_da_semana}, {data_dia_atual.date()}.")
        #print(dias)

    vendas = services.vendas.ver_vendas_intervalo(services.personal_prefs.get('vendedor'), 13, f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}")

    vendas_dia = []

    for dia in vendas:
        vendas_dia.append(dia['total'])

    data = {
        'Semana': ["Semana passada"] * 7 + ["Semana atual"] * 7,
        'Dia da semana': dia_da_semana * 2,
        'Vendas': vendas_dia[0:7] + vendas_dia[7:14]
    }

    df = pd.DataFrame(data)

    fig = px.line(df, x='Dia da semana', y='Vendas', color='Semana', title="Vendas semanais", markers=True, color_discrete_sequence=["#999999", "#999999"])
    fig.update_layout(
        dragmode=False,
        hovermode="x unified"
    )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_xaxes(
        showspikes=True,
        spikecolor="gray",
        spikesnap="data",
        spikemode="across",
        spikedash="dash",
    )

    ####################################################################

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

    return render_template("principais/graficos.html", base_url=base_url, pagina=pagina, fig_vendas=fig.to_html(full_html=False, include_plotlyjs='cdn'), estados_brasil=estados_brasil)

@app.route("/produtos")
@token_required
def produtos():
    pagina = "produtos"
    return render_template("principais/produtos.html", base_url=base_url, pagina=pagina)

@app.route("/anuncios")
@token_required
def anuncios():
    pagina = "anuncios"
    return render_template("principais/anuncios.html", base_url=base_url, pagina=pagina)

@app.route("/analise_mercado")
@token_required
def analise_mercado():
    pagina = "analise_mercado"
    return render_template("principais/analise_mercado.html", base_url=base_url, pagina=pagina)

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
    app.run(port=5050, debug=True)
