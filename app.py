import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diniz Health App", layout="wide")

# --- BANCO DE DADOS (SIMULADO/CSV) ---
def load_data():
    # Aqui o app carregaria o seu CSV consolidado
    data = {
        'data': ['09/01', '10/01', '11/01', '12/01', '13/01', '14/01', '15/01', '16/01', '17/01', '18/01'],
        'peso': [71.5, 71.2, 70.8, 70.5, 70.3, 70.25, 70.10, 69.90, 69.95, 69.90],
        'cals': [1500, 1600, 1450, 1550, 1600, 1450, 1478, 1715, 1800, 2159],
        'prot': [110, 120, 105, 115, 125, 95.5, 125.5, 127.8, 109.5, 111.3],
        'agua': [2500, 3100, 2800, 3200, 3000, 4850, 4700, 4150, 4050, 3210],
        'fibra': [20.0, 18.0, 22.0, 21.0, 20.0, 22.0, 34.5, 34.6, 28.0, 12.5],
        'carbo': [160, 165, 145, 155, 160, 150, 98.0, 157.0, 170.0, 262]
    }
    return pd.DataFrame(data)

df = load_data()
metas = {'peso': 67, 'cals': 1650, 'prot': 130, 'agua': 3000, 'fibra': 30, 'carbo': 150}
colors = {'peso': '#2ca02c', 'fibra': '#8b4513', 'prot': '#000000', 'carbo': '#ff7f0e', 'cals': '#d62728', 'agua': '#4682B4'}

# --- INTERFACE: OPÇÃO B (INPUT DE TEXTO) ---
st.markdown(f"### 🛡️ Tratamento Gástrico: Dia 5 de 28")
user_input = st.text_input("O que consumiu agora, Diniz?", placeholder="Ex: 300ml água e 150g frango")

if user_input:
    st.success(f"Registro processado: '{user_input}'")
    # Aqui entraria a lógica de Parser que treinamos para atualizar o CSV

# --- DASHBOARD VISUAL (PLOTLY INTERATIVO) ---
fig = go.Figure()

# Água (Área)
fig.add_trace(go.Scatter(x=df['data'], y=df['agua'], fill='tozeroy', name=f"Água (★ {metas['agua']})",
                         line=dict(color=colors['agua'], width=4), fillcolor='rgba(176, 224, 230, 0.3)'))

# Peso (Linha Verde)
fig.add_trace(go.Scatter(x=df['data'], y=df['peso'], name=f"Peso (★ {metas['peso']})",
                         line=dict(color=colors['peso'], width=6), marker=dict(size=12)))

# Proteína e Fibra (Barras)
fig.add_trace(go.Bar(x=df['data'], y=df['prot'], name=f"Proteína (★ {metas['prot']})", marker_color=colors['prot']))
fig.add_trace(go.Bar(x=df['data'], y=df['fibra'], name=f"Fibras (★ {metas['fibra']})", marker_color=colors['fibra']))

# Layout Centralizado (Conforme solicitado)
fig.update_layout(
    title={'text': "DASHBOARD CONSOLIDADO: METAS ESTRELA", 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
    legend=dict(orientation="h", yanchor="bottom", y=0.85, xanchor="center", x=0.5, bgcolor="rgba(255,255,255,0.8)"),
    height=700,
    template="plotly_white"
)

# Estrelas nos Eixos
fig.update_yaxes(tickvals=[metas['peso'], metas['prot'], metas['fibra']], 
                 ticktext=[f"★ {metas['peso']}", f"★ {metas['prot']}", f"★ {metas['fibra']}"])

st.plotly_chart(fig, use_container_width=True)
