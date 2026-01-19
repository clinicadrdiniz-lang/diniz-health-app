import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Diniz Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. LINK DA PLANILHA
url = "https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing"

@st.cache_data(ttl=60) # Atualiza a cada 1 minuto se houver mudanças
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
        h1 { color: #00BFFF; text-align: center; font-family: 'Helvetica'; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Diniz Performance Dashboard")

    # 3. CRIAÇÃO DO GRÁFICO COM EIXO DUPLO (RESOLVE A DESPROPORÇÃO)
    # Eixo 1: Peso | Eixo 2: Calorias, Proteínas e Água
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # CALORIAS (Barras Laranja - Escala de 0 a 2500+)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Calorias'],
        name='🔥 Calorias (kcal)', marker_color='#FF8C00', opacity=0.5
    ), secondary_y=True)

    # PROTEÍNAS (Barras Brancas - Sobrepostas para volume visual)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'],
        name='🥩 Proteína (g)', marker_color='#FFFFFF', opacity=0.9
    ), secondary_y=True)

    # ÁGUA (Linha Azul Neon - Área preenchida)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água (ml)', line=dict(color='#00BFFF', width=2),
        opacity=0.2
    ), secondary_y=True)

    # PESO (Linha Verde Neon - EIXO INDEPENDENTE À ESQUERDA)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'],
        name='⚖️ Peso (kg)', line=dict(color='#39FF14', width=6),
        mode='lines+markers+text', 
        text=df['Peso'], textposition="top center",
        textfont=dict(color='#39FF14', size=14)
    ), secondary_y=False)

    # 4. AJUSTE DE LAYOUT E ESCALAS
    fig.update_layout(
        plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
        font_color='#FFFFFF', height=750,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        hovermode="x unified",
        barmode='overlay' # Sobrepõe as barras para não ficarem "magras"
    )

    # Configuração de Eixos (Aqui está o segredo da proporção)
    fig.update_yaxes(title_text="<b>Peso (kg)</b>", color="#39FF14", secondary_y=False, showgrid=False, range=[60, 80])
    fig.update_yaxes(title_text="<b>Consumo Diário</b>", color="#FFFFFF", secondary_y=True, gridcolor='#222222')

    # Linhas de Meta (Targets)
    fig.add_hline(y=1650, line_dash="dot", line_color="#FF8C00", annotation_text="Meta Kcal", secondary_y=True)
    fig.add_hline(y=130, line_dash="dot", line_color="#FFFFFF", annotation_text="Meta Prot", secondary_y=True)
    fig.add_hline(y=3000, line_dash="dot", line_color="#00BFFF", annotation_text="Meta Água", secondary_y=True)

    # Mostrar o Gráfico
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 5. RESUMO DE HOJE (Métricas)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    ult = df.iloc[-1]
    
    c1.metric("⚖️ PESO", f"{ult['Peso']}kg")
    c2.metric("💧 ÁGUA", f"{int(ult['Agua'])}ml")
    c3.metric("🔥 CALORIAS", f"{int(ult['Calorias'])}kcal")
    c4.metric("🥩 PROT", f"{int(ult['Proteinas'])}g")

except Exception as e:
    st.error(f"Erro na Planilha: {e}")
    st.info("Verifique se os nomes das colunas são: Data, Peso, Agua, Proteinas, Calorias, Carbos")

st.markdown("<p style='text-align: center; color: #444444;'>Sistema de Performance Dr. Diniz</p>", unsafe_allow_html=True)
