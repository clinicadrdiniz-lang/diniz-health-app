import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Diniz Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. LINK DA PLANILHA
url = "https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing"

@st.cache_data(ttl=60)
def carregar_dados(url_link):
    csv_url = url_link.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

try:
    df = carregar_dados(url)
    
    # --- ESTILO DARK MODE ---
    st.markdown("""
        <style>
        .main { background-color: #0E1117; }
        .stApp { background-color: #0E1117; }
        h1 { color: #00BFFF; text-align: center; margin-bottom: 0px; }
        [data-testid="stMetricValue"] { font-size: 22px !important; color: #FFFFFF !important; }
        [data-testid="stMetricLabel"] { color: #888888 !important; }
        hr { border-color: #333333 !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Diniz Performance Dashboard")

    # 3. CRIAÇÃO DO GRÁFICO (EIXO DUPLO PARA PROPORÇÃO)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # BARRAS AGRUPADAS (Macros e Calorias) - Eixo Secundário (Direita)
    # Calorias
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Calorias'],
        name='🔥 Kcal', marker_color='#FF8C00', opacity=0.6
    ), secondary_y=True)

    # Proteínas
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'],
        name='🥩 Prot', marker_color='#FFFFFF', opacity=0.9
    ), secondary_y=True)

    # Carboidratos
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Carbos'],
        name='🍞 Carb', marker_color='#FFFF00', opacity=0.8
    ), secondary_y=True)

    # Fibras
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Fibras'],
        name='🥗 Fibra', marker_color='#CD853F', opacity=0.9
    ), secondary_y=True)

    # ÁGUA (Área fluida ao fundo)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água', line=dict(color='#00BFFF', width=1),
        opacity=0.15
    ), secondary_y=True)

    # PESO (Linha Verde Neon - Eixo Principal à Esquerda)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'],
        name='⚖️ Peso', line=dict(color='#39FF14', width=6),
        mode='lines+markers+text', 
        text=df['Peso'], textposition="top center",
        textfont=dict(color='#39FF14', size=14)
    ), secondary_y=False)

    # 4. CONFIGURAÇÃO DE LAYOUT (MODO DARK)
    fig.update_layout(
        plot_bgcolor='#0E1117', 
        paper_bgcolor='#0E1117',
        font_color='#FFFFFF', 
        height=750,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        hovermode="x unified",
        barmode='group', # Barras lado a lado
        bargap=0.15
    )

    # Ajuste de eixos (Peso à esquerda, Consumos ocultos à direita para limpeza)
    fig.update_yaxes(title_text="Peso (kg)", secondary_y=False, showgrid=False, range=[60, 85], color="#39FF14")
    fig.update_yaxes(secondary_y=True, showgrid=True, gridcolor='#222222', showticklabels=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. PAINEL DE MÉTRICAS (GRID 2 linhas x 3 colunas)
    st.markdown("---")
    ult = df.iloc[-1]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("⚖️ PESO", f"{ult['Peso']}kg")
    c2.metric("🔥 KCAL", f"{int(ult['Calorias'])}kcal")
    c3.metric("💧 ÁGUA", f"{int(ult['Agua'])}ml")
    
    c4, c5, c6 = st.columns(3)
    c4.metric("🥩 PROT", f"{int(ult['Proteinas'])}g")
    c5.metric("🍞 CARB", f"{int(ult['Carbos'])}g")
    c6.metric("🥗 FIBRA", f"{ult['Fibras']}g")

except Exception as e:
    st.error(f"Erro: {e}")
    st.info("Dica: Certifique-se que a planilha tem as colunas: Data, Peso, Agua, Proteinas, Calorias, Carbos, Fibras")

st.markdown("<p style='text-align: center; color: #444444; font-size: 11px;'>Sincronizado via Google Sheets | Dr. Diniz</p>", unsafe_allow_html=True)
