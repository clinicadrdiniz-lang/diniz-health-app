import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diniz Health App", layout="wide", page_icon="🛡️")

# --- CONEXÃO COM O CÉREBRO (GOOGLE SHEETS) ---
# Substitua o link abaixo pelo link da sua planilha
url = https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url)
    # Limpeza básica de dados
    df.columns = df.columns.str.strip() 
except:
    st.error("Erro ao conectar com a Google Sheet. Verifique o link e as permissões.")
    st.stop()

# --- DEFINIÇÕES DE METAS (ESTRELAS ★) ---
metas = {'peso': 67.0, 'cals': 1650, 'prot': 130, 'agua': 3000, 'fibra': 30, 'carbo': 150}
colors = {
    'peso': '#2ca02c', 'fibra': '#8b4513', 'prot': '#000000', 
    'carbo': '#ff7f0e', 'cals': '#d62728', 'agua_line': '#4682B4', 'agua_fill': '#B0E0E6'
}

# --- INTERFACE DE USUÁRIO (OPÇÃO B) ---
st.markdown(f"### 🛡️ Diniz Health App | Controle Gástrico (Dia 5)")

# Campo de entrada centralizado
user_input = st.text_input("O que consumiu agora, Diniz?", placeholder="Ex: 500ml água e 1 Heineken")

if user_input:
    st.success(f"Recebido: '{user_input}'. Atualize a planilha para ver no gráfico!")

# --- CONSTRUÇÃO DO DASHBOARD (PLOTLY) ---
fig = go.Figure()

# 1. Água (Área Azul)
fig.add_trace(go.Scatter(
    x=df['Data'], y=df['Agua'], fill='tozeroy', 
    name=f"Água (★ {int(metas['agua'])})",
    line=dict(color=colors['agua_line'], width=4),
    fillcolor='rgba(176, 224, 230, 0.4)'
))

# 2. Peso (Linha Verde com Pontos)
fig.add_trace(go.Scatter(
    x=df['Data'], y=df['Peso'], name=f"Peso (★ {int(metas['peso'])})",
    line=dict(color=colors['peso'], width=6),
    marker=dict(size=12, symbol='circle')
))

# 3. Proteína (Barras Pretas)
fig.add_trace(go.Bar(
    x=df['Data'], y=df['Proteinas'], name=f"Proteína (★ {int(metas['prot'])})",
    marker_color=colors['prot'], opacity=0.8
))

# 4. Fibras (Barras Marrons)
fig.add_trace(go.Bar(
    x=df['Data'], y=df['Fibras'], name=f"Fibras (★ {int(metas['fibra'])})",
    marker_color=colors['fibra'], opacity=0.8
))

# --- LAYOUT FINAL (CENTRALIZADO) ---
fig.update_layout(
    title={'text': "DASHBOARD CONSOLIDADO: METAS ESTRELA", 'y':0.95, 'x':0.5, 'xanchor': 'center'},
    legend=dict(
        orientation="h", yanchor="bottom", y=0.88, xanchor="center", x=0.5,
        font=dict(size=14, color="black"), borderwidth=1
    ),
    margin=dict(l=20, r=20, t=100, b=20),
    hovermode="x unified",
    template="plotly_white",
    height=750
)

# Adicionando as Estrelas nos Eixos Y
fig.update_yaxes(tickvals=[metas['peso'], metas['prot'], metas['agua'], metas['cals']],
                 ticktext=[f"★ {metas['peso']}", f"★ {metas['prot']}", f"★ {metas['agua']}", f"★ {metas['cals']}"])

# Exibir Gráfico
st.plotly_chart(fig, use_container_width=True)

# --- RODAPÉ DE STATUS ---
hoje = df.iloc[-1]
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Água Total", f"{int(hoje['Agua'])} ml", delta=f"{int(hoje['Agua'] - metas['agua'])} ml")
c2.metric("Peso Atual", f"{hoje['Peso']} kg", delta=f"{round(hoje['Peso'] - metas['peso'], 2)} kg", delta_color="inverse")
c3.metric("Proteína", f"{int(hoje['Proteinas'])} g")
c4.metric("Fibras", f"{hoje['Fibras']} g")
