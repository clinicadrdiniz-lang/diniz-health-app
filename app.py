import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA (Ajusta o título na aba do navegador)
st.set_page_config(page_title="Diniz Health App", layout="wide", initial_sidebar_state="collapsed")

# 2. LINK DA PLANILHA (Sua Google Sheet)
url = "https://docs.google.com/spreadsheets/d/10Jx1PiZmb_IEYSXXqJdi2UDMdknmPytE-gSoqfY-kK8/edit?usp=sharing"

# 3. ALGORITMO DE VELOCIDADE (Cache de 10 minutos)
@st.cache_data(ttl=600)
def carregar_dados(url_link):
    # Converte link de visualização em link de download direto para o Python
    csv_url = url_link.replace('/edit?usp=sharing', '/export?format=csv')
    data = pd.read_csv(csv_url)
    return data

# Tenta carregar os dados
try:
    df = carregar_dados(url)
    
    # --- INTERFACE DARK MODE ---
    st.markdown("""
        <style>
        .main { background-color: #111111; }
        .stApp { background-color: #111111; }
        h1 { color: #00BFFF; font-family: 'sans serif'; }
        </style>
    """, unsafe_allow_stdio=True)

    st.title("🚀 Diniz Performance Dashboard")

    # 4. CRIAÇÃO DO GRÁFICO (MODO DARK NEON)
    fig = go.Figure()

    # Água (Área Azul Neon)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Agua'], fill='tozeroy',
        name='Água (ml)', line=dict(color='#00BFFF', width=4),
        hovertemplate='%{y}ml'
    ))

    # Peso (Linha Verde Neon)
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Peso'], name='Peso (kg)',
        line=dict(color='#39FF14', width=6),
        hovertemplate='%{y}kg'
    ))

    # Proteína (Barras Brancas de Alta Visibilidade)
    fig.add_trace(go.Bar(
        x=df['Data'], y=df['Proteinas'], name='Proteína (g)',
        marker_color='#FFFFFF', opacity=0.8,
        hovertemplate='%{y}g'
    ))

    # 5. LAYOUT E ESTÉTICA
    fig.update_layout(
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font_color='#FFFFFF',
        height=750,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(gridcolor='#333333', tickfont=dict(size=14)),
        hovermode="x unified"
    )

    # Adicionar Linhas de Meta (Estrelas ★)
    fig.add_hline(y=3000, line_dash="dot", line_color="#00BFFF", 
                  annotation_text="Meta Água (3L)", annotation_font_color="#00BFFF")
    fig.add_hline(y=130, line_dash="dot", line_color="#FFFFFF", 
                  annotation_text="Meta Proteína (130g)", annotation_font_color="#FFFFFF")

    # Mostrar o Gráfico
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 6. MÉTRICAS RÁPIDAS (RESUMO FINAL)
    col1, col2, col3 = st.columns(3)
    ultimo_peso = df['Peso'].iloc[-1]
    ultima_agua = df['Agua'].iloc[-1]
    
    col1.metric("Peso Atual", f"{ultimo_peso} kg", delta_color="inverse")
    col2.metric("Hidratação", f"{ultima_agua} ml", delta=f"{ultima_agua-3000} ml")
    col3.metric("Status", "🔥 Em Alta Performance")

except Exception as e:
    st.error(f"Erro ao ler a planilha: {e}")
    st.info("Verifique se os títulos das colunas na planilha são: Data, Peso, Agua, Proteinas, Fibras, Carbos")

# Rodapé discreto
st.markdown("<p style='text-align: center; color: #555555;'>Atualizado em tempo real via Google Sheets</p>", unsafe_allow_html=True)
