import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import requests
import json
import re

# Configuração
st.set_page_config(page_title="Método Babi - Monitoramento IA", layout="wide")

# Database Setup
def init_db():
    conn = sqlite3.connect('babi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS noticias
                 (data TEXT, link TEXT, relevancia TEXT, resumo TEXT, 
                  fortalezas TEXT, fraquezas TEXT, publico TEXT, 
                  colaboracao TEXT, periodo TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# Tabs
tabs = st.tabs(["Configuração + Fontes", "Dashboard", "Data Lab", "Decision Make"])

# 1️⃣ Configuração
with tabs[0]:
    st.header("🔧 Configuração e Fontes")
    
    col1, col2 = st.columns(2)
    with col1:
        keywords = st.text_area("Palavras-chave", "IA, mercado, inovação")
    with col2:
        fontes = st.text_area("Fontes", "google.com, notion.so")
    
    if st.button("Salvar"):
        st.session_state.update({'keywords': keywords, 'fontes': fontes})
        st.success("✅ Configuração salva!")

# 2️⃣ Dashboard
with tabs[1]:
    st.header("📊 Dashboard")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        relevancia_filter = st.selectbox("Relevância", ["Todos", "Bomba", "Alta", "Média", "Baixa"])
    with col2:
        data_filter = st.date_input("Data Inicial")
    with col3:
        export = st.button("📥 Exportar CSV")
    
    # Visualizações
    if st.button("+ Nova Notícia"):
        with st.form("nova_noticia"):
            data = st.date_input("Data")
            link = st.text_input("Link")
            relevancia = st.selectbox("Relevância", ["Bomba", "Alta", "Média", "Baixa"])
            resumo = st.text_area("Resumo")
            
            if st.form_submit_button("Salvar"):
                c = conn.cursor()
                c.execute('''INSERT INTO noticias VALUES 
                           (?,?,?,?,?,?,?,?,?)''', 
                           (data.strftime("%Y-%m-%d"), link, relevancia, 
                            resumo, "", "", "", "", ""))
                conn.commit()
                st.success("Notícia salva!")
    
    # Tabela e Gráficos
    c = conn.cursor()
    dados = c.execute("SELECT * FROM noticias").fetchall()
    if dados:
        df = pd.DataFrame(dados, columns=['Data', 'Link', 'Relevância', 'Resumo', 
                                        'Fortalezas', 'Fraquezas', 'Público',
                                        'Colaboração', 'Período'])
        
        # Gráfico de tendências
        fig = px.line(df, x='Data', y='Relevância', title='Tendência de Relevância')
        st.plotly_chart(fig)
        
        # Tabela com paginação
        page_size = 10
        page = st.number_input('Página', min_value=1, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        st.dataframe(df.iloc[start_idx:end_idx])

# 3️⃣ Data Lab
with tabs[2]:
    st.header("🔬 Data Lab")
    
    user_input = st.chat_input("Análise de tendências...")
    
    if user_input:
        with st.spinner("Analisando..."):
            # Simulação de análise de sentimento
            sentiment = "Positivo" if "bom" in user_input.lower() else "Negativo"
            st.info(f"Sentimento detectado: {sentiment}")
            
            # Chamada API
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "sonar-reasoning-pro",
                    "messages": [{"role": "user", "content": user_input}]
                }
            )
            
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                with st.chat_message("assistant"):
                    st.write(reply)
                    
                # Análise de tópicos
                topics = [word for word in user_input.split() if len(word) > 3]
                st.bar_chart(pd.DataFrame({'tópico': topics, 'frequência': [1]*len(topics)}).set_index('tópico'))

# 4️⃣ Decision Make
with tabs[3]:
    st.header("🤖 Decision Make")
    
    col1, col2 = st.columns(2)
    with col1:
        decision = st.selectbox("Ação", ["Campanha", "Novos Mercados", "Produto"])
        impact = st.slider("Impacto Esperado", 0, 100)
    
    with col2:
        st.metric("Confiança IA", f"{impact}%")
        if st.button("Confirmar"):
            st.balloons()
            st.success(f"Ação '{decision}' registrada!")
