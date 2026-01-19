import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Diniz Health Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. LINK DA PLANILHA
url = "https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing"

# 3. ALGORITMO DE VELOCIDADE (Cache de 10 min)
@st.cache_data(ttl=600)
def carregar_dados(url_link):
    csv_url = url_link.replace('/edit?usp=sharing', '/export?format=csv')
    data = pd.read_csv(csv_url)
    return data

try:
    df = carregar_dados(url)
    
    # --- INTERFACE DARK MODE ---
    st.markdown("""
        <style>
        .main { background-color: #0E1117; }
        .stApp { background-color: #0E1117; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 28px !important; }
        [data-testid="stMetricLabel"] { color: #888888 !important; }
        h1 { color: #00BFFF; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Diniz Performance Dashboard")

    # 4. GRÁFICO MULTI-MÉTRICAS NEON
    fig = go.Figure()

    # Água (Área Azul)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='Água (ml)', line=dict(color='#00BFFF', width=2),
        opacity=0.3
    ))

    # Calorias (Linha Laranja Neon) - Nova Métrica
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Carbos'], # Se sua coluna de calorias tiver outro nome na planilha, mude aqui
        name='Calorias (kcal)', line=dict(color='#FF8C00', width=5),
        mode='lines+markers'
    ))

    # Peso (Linha Verde Neon)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'], name='Peso (kg)',
        line=dict(color='#39FF14', width=5),
        mode='lines+markers'
    ))

    # Proteína (Barras Brancas)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'], name='Proteína (g)',
        marker_color='#FFFFFF', opacity=0.7
    ))

    # 5. LAYOUT DARK MODE
    fig.update_layout(
        plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
        font_color='#FFFFFF', height=700,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#222222'),
        hovermode="x unified"
    )

    # Linhas de Meta (Targets)
    fig.add_hline(y=3000, line_dash="dot", line_color="#00BFFF", annotation_text="Meta Água")
    fig.add_hline(y=130, line_dash="dot", line_color="#FFFFFF", annotation_text="Meta Prot")
    fig.add_hline(y=1650, line_dash="dot", line_color="#FF8C00", annotation_text="Meta Kcal")

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 6. CARTÕES DE MÉTRICAS (RODAPÉ)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    
    # Busca o último valor de cada coluna
    ultimo_peso = df['Peso'].iloc[-1]
    ultima_agua = df['Agua'].iloc[-1]
    # Aqui assume-se que usa a coluna 'Carbos' ou 'Calorias' na sua planilha
    ultima_kcal = df['Carbos'].iloc[-1] if 'Carbos' in df.columns else 0

    c1.metric("⚖️ PESO", f"{ultimo_peso} kg")
    c2.metric("💧 ÁGUA", f"{ultima_agua} ml")
    c3.metric("🔥 CALORIAS", f"{int(ultima_kcal)} kcal")

except Exception as e:
    st.error(f"Erro ao ler a planilha: {e}")
    st.info("Dica: Verifique se os nomes das colunas na Planilha estão corretos (Data, Peso, Agua, Proteinas, Carbos)")

st.markdown("<p style='text-align: center; color: #444444; font-size: 12px;'>Sincronizado via Google Sheets API</p>", unsafe_allow_html=True)
