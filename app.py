import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Nutri_Diniz", layout="wide", initial_sidebar_state="collapsed")

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
        h1 { color: #00BFFF; text-align: center; font-family: 'Trebuchet MS'; font-weight: bold; }
        [data-testid="stMetricValue"] { font-size: 20px !important; color: #FFFFFF !important; }
        [data-testid="stMetricLabel"] { color: #888888 !important; }
        </style>
    """, unsafe_allow_html=True)

    # TÍTULO SOLICITADO
    st.title("🍎 Nutri_Diniz Performance")

    # 3. CRIAÇÃO DO GRÁFICO (DOIS EIXOS PARA PROPORÇÃO)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # BARRAS AGRUPADAS (Eixo Secundário)
    # Calorias
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Calorias'],
        name='🔥 Calorias', marker_color='#FF8C00', opacity=0.6
    ), secondary_y=True)

    # Proteínas
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'],
        name='🥩 Proteínas', marker_color='#FFFFFF', opacity=0.9
    ), secondary_y=True)

    # Carboidratos
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Carbos'],
        name='🍞 Carbos', marker_color='#FFFF00', opacity=0.8
    ), secondary_y=True)

    # Fibras
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Fibras'],
        name='🥗 Fibras', marker_color='#CD853F', opacity=0.9
    ), secondary_y=True)

    # ÁGUA (Área ao fundo)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água', line=dict(color='#00BFFF', width=1),
        opacity=0.1
    ), secondary_y=True)

    # PESO (Linha de Destaque - Eixo Principal)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'],
        name='⚖️ Peso', line=dict(color='#39FF14', width=6),
        mode='lines+markers+text', 
        text=df['Peso'], textposition="top center",
        textfont=dict(color='#39FF14')
    ), secondary_y=False)

    # 4. CONFIGURAÇÃO DE LAYOUT
    fig.update_layout(
        plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
        font_color='#FFFFFF', height=750,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        hovermode="x unified",
        barmode='group',
        bargap=0.15
    )

    # Ajuste de eixos (Foco no Peso à esquerda)
    fig.update_yaxes(title_text="Peso (kg)", secondary_y=False, showgrid=False, range=[60, 85], color="#39FF14")
    fig.update_yaxes(secondary_y=True, showgrid=True, gridcolor='#222222', showticklabels=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. CARTÕES DE MÉTRICAS RÁPIDAS
    st.markdown("---")
    ult = df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("⚖️ PESO", f"{ult['Peso']}kg")
    col2.metric("🔥 KCAL", f"{int(ult['Calorias'])}kcal")
    col3.metric("💧 ÁGUA", f"{int(ult['Agua'])}ml")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("🥩 PROT", f"{int(ult['Proteinas'])}g")
    col5.metric("🍞 CARB", f"{int(ult['Carbos'])}g")
    col6.metric("🥗 FIBRA", f"{ult['Fibras']}g")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")

st.markdown("<p style='text-align: center; color: #444444; font-size: 11px;'>Nutri_Diniz v2.0 - Performance Control</p>", unsafe_allow_html=True)
