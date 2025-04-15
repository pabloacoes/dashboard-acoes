import streamlit as st
import yfinance as yf
import pandas as pd
import math

st.set_page_config(page_title="Valuation Graham e Bazin", layout="wide")

st.title("Valuation de Ações - Graham e Bazin")

# Entrada do usuário
tickers_input = st.text_input("Digite os tickers separados por vírgula (ex: ITSA4.SA, PETR4.SA, WEGE3.SA)", "ITSA4.SA, PETR4.SA, WEGE3.SA")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

# Funções
def calcular_preco_justo(lpa, vpa):
    try:
        return math.sqrt(22.5 * lpa * vpa)
    except:
        return None

def calcular_preco_teto(dividendos):
    return (dividendos * 100) / 6

# Coleta de dados
dados_acoes = []

for ticker in tickers:
    try:
        acao = yf.Ticker(ticker)
        info = acao.info

        lpa = info.get("trailingEps", 0)
        vpa = info.get("bookValue", 0)
        dividendos = info.get("dividendRate", 0)
        preco_justo = calcular_preco_justo(lpa, vpa)
        preco_teto = calcular_preco_teto(dividendos)

        dados_acoes.append({
            "Ação": ticker,
            "LPA (R$)": round(lpa, 2),
            "VPA (R$)": round(vpa, 2),
            "Dividendos (R$)": round(dividendos, 2),
            "Preço Justo (Graham)": round(preco_justo, 2) if preco_justo else "N/A",
            "Preço Teto (Bazin)": round(preco_teto, 2)
        })
    except Exception as e:
        st.error(f"Erro ao obter dados de {ticker}: {e}")

# Exibe os dados em tabela
df = pd.DataFrame(dados_acoes)
st.dataframe(df, use_container_width=True)

# Download
st.download_button(
    label="Baixar Excel",
    data=df.to_excel(index=False, engine='openpyxl'),
    file_name="avaliacao_acoes.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
