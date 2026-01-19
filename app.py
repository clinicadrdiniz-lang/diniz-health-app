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
    
    # --- ESTILO FUNDO BRANCO ---
    st.markdown("""
        <style>
        .main { background-color: #FFFFFF; }
        .stApp { background-color: #FFFFFF; }
        h1 { color: #1E1E1E; text-align: center; font-family: 'Helvetica'; }
        [data-testid="stMetricValue"] { color: #1E1E1E !important; font-size: 20px !important; }
        [data-testid="stMetricLabel"] { color: #555555 !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Diniz Performance Dashboard")

    # 3. CRIAÇÃO DO GRÁFICO (EIXO DUPLO)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # BARRAS AGRUPADAS (Macros e Calorias) - Eixo Secundário
    # Calorias (Laranja)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Calorias'],
        name='🔥 Kcal', marker_color='#FF8C00', opacity=0.8
    ), secondary_y=True)

    # Proteínas (Cinza Escuro para destacar no branco)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'],
        name='🥩 Prot', marker_color='#333333', opacity=0.9
    ), secondary_y=True)

    # Carboidratos (Amarelo Ouro)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Carbos'],
        name='🍞 Carb', marker_color='#FFD700', opacity=0.8
    ), secondary_y=True)

    # Fibras (Verde Musgo)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Fibras'],
        name='🥗 Fibra', marker_color='#228B22', opacity=0.8
    ), secondary_y=True)

    # ÁGUA (Área Azul Suave)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água', line=dict(color='#00BFFF', width=1),
        opacity=0.2
    ), secondary_y=True)

    # PESO (Linha de Tendência - Verde Forte)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'],
        name='⚖️ Peso', line=dict(color='#006400', width=5),
        mode='lines+markers+text', 
        text=df['Peso'], textposition="top center",
        textfont=dict(color='#006400', size=12)
    ), secondary_y=False)

    # 4. CONFIGURAÇÃO DE LAYOUT (FUNDO BRANCO)
    fig.update_layout(
        plot_bgcolor='#FFFFFF', 
        paper_bgcolor='#FFFFFF',
        font_color='#1E1E1E', 
        height=700,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        hovermode="x unified",
        barmode='group',
        bargap=0.15
    )

    # Ajuste de eixos e grelha (cinza claro para não poluir)
    fig.update_yaxes(title_text="Peso (kg)", secondary_y=False, showgrid=True, gridcolor='#EEEEEE', range=[60, 80])
    fig.update_yaxes(secondary_y=True, showgrid=False, showticklabels=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. PAINEL DE MÉTRICAS (GRID 3x2)
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

st.markdown("<p style='text-align: center; color: #888888; font-size: 12px;'>Dashboard Dr. Diniz Performance</p>", unsafe_allow_html=True)
