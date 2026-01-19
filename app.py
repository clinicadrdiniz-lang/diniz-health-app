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
        [data-testid="stMetricValue"] { font-size: 18px !important; color: #FFFFFF !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🍎 Nutri_Diniz Performance")

    # 3. CRIAÇÃO DO GRÁFICO COM EIXOS INDEPENDENTES
    # Criamos uma base com eixos secundários
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # SÉRIE 1: Água (Eixo Secundário - Azul)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água', line=dict(color='#00BFFF', width=1),
        opacity=0.1
    ), secondary_y=True)

    # SÉRIE 2: Calorias (Eixo Secundário - Laranja)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Calorias'],
        name='🔥 Kcal', marker_color='#FF8C00', opacity=0.4
    ), secondary_y=True)

    # SÉRIE 3: Proteínas (Eixo Secundário - Branco)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'],
        name='🥩 Prot', marker_color='#FFFFFF', opacity=0.7
    ), secondary_y=True)

    # SÉRIE 4: Carbos (Eixo Secundário - Amarelo)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Carbos'],
        name='🍞 Carb', marker_color='#FFFF00', opacity=0.5
    ), secondary_y=True)

    # SÉRIE 5: Peso (EIXO PRINCIPAL - Verde Neon)
    # Aqui o peso ganha sua própria escala à esquerda
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'],
        name='⚖️ Peso', line=dict(color='#39FF14', width=6),
        mode='lines+markers+text', 
        text=df['Peso'], textposition="top center",
        textfont=dict(color='#39FF14', size=14)
    ), secondary_y=False)

    # 4. AJUSTE DE LAYOUT E PROPORÇÕES
    fig.update_layout(
        plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
        font_color='#FFFFFF', height=750,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        hovermode="x unified",
        barmode='overlay' # Sobrepõe para cada escala se ajustar sozinha
    )

    # Configuração dos Eixos Y (O segredo do ajuste de tela)
    fig.update_yaxes(title_text="<b>PESO (Escala 1)</b>", color="#39FF14", secondary_y=False, showgrid=False, range=[df['Peso'].min()-1, df['Peso'].max()+1])
    fig.update_yaxes(title_text="<b>CONSUMO (Escala 2)</b>", secondary_y=True, showgrid=True, gridcolor='#222222', showticklabels=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. PAINEL DE MÉTRICAS RÁPIDAS
    st.markdown("---")
    ult = df.iloc[-1]
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("PESO", f"{ult['Peso']}k")
    c2.metric("KCAL", f"{int(ult['Calorias'])}")
    c3.metric("ÁGUA", f"{int(ult['Agua'])}")
    c4.metric("PROT", f"{int(ult['Proteinas'])}g")
    c5.metric("CARB", f"{int(ult['Carbos'])}g")
    c6.metric("FIB", f"{ult['Fibras']}g")

except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("<p style='text-align: center; color: #444444; font-size: 10px;'>Nutri_Diniz v3.0 - Multi-Axis System</p>", unsafe_allow_html=True)