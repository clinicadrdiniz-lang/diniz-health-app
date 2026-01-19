import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Diniz Health Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. LINK DA PLANILHA (Sua Google Sheet)
url = "https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing"

# 3. ALGORITMO DE VELOCIDADE (Cache de 10 min para abertura instantânea)
@st.cache_data(ttl=600)
def carregar_dados(url_link):
    # Converte link de visualização em link de download direto
    csv_url = url_link.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url)

try:
    df = carregar_dados(url)
    
    # --- ESTILIZAÇÃO INTERFACE DARK MODE ---
    st.markdown("""
        <style>
        .main { background-color: #0E1117; }
        .stApp { background-color: #0E1117; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 26px !important; }
        [data-testid="stMetricLabel"] { color: #888888 !important; }
        h1 { color: #00BFFF; text-align: center; font-family: 'Helvetica'; padding-bottom: 0px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Diniz Performance Dashboard")

    # 4. CRIAÇÃO DO GRÁFICO MULTI-SÉRIES
    fig = go.Figure()

    # SÉRIE 1: Água (Área Azul)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='💧 Água (ml)', line=dict(color='#00BFFF', width=2),
        opacity=0.3
    ))

    # SÉRIE 2: Calorias (Linha Laranja Neon)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Calorias'], 
        name='🔥 Calorias (kcal)', line=dict(color='#FF8C00', width=4),
        mode='lines+markers'
    ))

    # SÉRIE 3: Peso (Linha Verde Neon)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'], 
        name='⚖️ Peso (kg)', line=dict(color='#39FF14', width=5),
        mode='lines+markers'
    ))

    # SÉRIE 4: Proteínas (Barras Brancas)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'], 
        name='🥩 Proteína (g)', marker_color='#FFFFFF', opacity=0.6
    ))

    # SÉRIE 5: Carbos (Linha Amarela Fina)
    if 'Carbos' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['Data'], y=df['Carbos'], 
            name='🍞 Carbos (g)', line=dict(color='#FFFF00', width=2, dash='dot')
        ))

    # 5. LAYOUT E DESIGN DARK
    fig.update_layout(
        plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
        font_color='#FFFFFF', height=700,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(gridcolor='#222222', tickfont=dict(size=12)),
        hovermode="x unified"
    )

    # Linhas de Meta (Targets Pontilhados)
    fig.add_hline(y=3000, line_dash="dot", line_color="#00BFFF", annotation_text="Meta Água")
    fig.add_hline(y=130, line_dash="dot", line_color="#FFFFFF", annotation_text="Meta Prot")
    fig.add_hline(y=1650, line_dash="dot", line_color="#FF8C00", annotation_text="Meta Kcal")

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 6. PAINEL DE MÉTRICAS RÁPIDAS (Último Registro)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    
    ultimo = df.iloc[-1]
    
    c1.metric("PESO", f"{ultimo['Peso']}kg")
    c2.metric("ÁGUA", f"{int(ultimo['Agua'])}ml")
    c3.metric("CALORIAS", f"{int(ultimo['Calorias'])}kcal")
    c4.metric("PROT", f"{int(ultimo['Proteinas'])}g")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
    st.info("Verifique se as colunas na planilha são: Data, Peso, Agua, Proteinas, Calorias, Carbos")

st.markdown("<p style='text-align: center; color: #555555; font-size: 12px;'>Sincronizado via Google Sheets | Dr. Diniz Performance</p>", unsafe_allow_html=True)
