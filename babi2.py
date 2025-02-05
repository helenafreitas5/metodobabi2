import streamlit as st
import requests
import json
import re
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Método Babi - Monitoramento IA", layout="wide")

# Carregar chave da API do Streamlit Secrets
API_KEY = st.secrets["perplexity"]["API_KEY"]
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Inicializar sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "noticias" not in st.session_state:
    st.session_state.noticias = []

# Criar Tabs de Navegação
tabs = st.tabs(["Configuração + Fontes", "Dashboard", "Data Lab", "Decision Make"])

# 1️⃣ Configuração + Fontes
with tabs[0]:
    st.header("🔧 Configuração e Fontes de Dados")
    st.write("Defina palavras-chave e fontes de coleta de dados para o monitoramento.")

    keywords = st.text_area("Palavras-chave para monitoramento", "inteligência artificial, mercado, inovação")
    fontes = st.text_area("Fontes de notícias (ex: Google Alerts, Notion)", "google.com, notion.so")

    if st.button("Salvar Configuração"):
        st.session_state.keywords = keywords
        st.session_state.fontes = fontes
        st.success("Configuração salva com sucesso!")

# 2️⃣ Dashboard
with tabs[1]:
    st.header("📊 Dashboard - Monitoramento de Notícias")
    st.write("Visualização das últimas notícias categorizadas pela IA.")

    if st.button("Adicionar Notícia Simulada"):
        st.session_state.noticias.append({
            "Data": datetime.now().strftime("%Y-%m-%d"),
            "Link": "https://exemplo.com/noticia",
            "Relevância": "Bomba",
            "Resumo": "Nova tendência no mercado AI!",
            "Fortalezas": "Alto impacto",
            "Fraquezas": "Alto risco",
            "Público-alvo": "Empresas de tecnologia",
            "Colaboração": "Nenhuma",
            "Período da Ação": "Q1 2025"
        })

    if st.session_state.noticias:
        st.table(st.session_state.noticias)
    else:
        st.warning("Nenhuma notícia cadastrada ainda.")

# 3️⃣ Data Lab
with tabs[2]:
    st.header("🔬 Data Lab - Análise Semântica e IA")
    st.write("Análise semântica com InfraNodus e respostas da API Perplexity.")

    user_input = st.chat_input("Pergunte sobre as tendências do mercado...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        payload = {
            "model": "sonar-reasoning-pro",
            "messages": st.session_state.messages
        }

        response = requests.post("https://api.perplexity.ai/chat/completions", headers=HEADERS, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            reply = response_data["choices"][0]["message"]["content"]
            sources = response_data.get("sources", [])

            reply_cleaned = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()

            st.session_state.messages.append({"role": "assistant", "content": reply_cleaned})

            with st.expander("💡 **Resposta da Perplexity**"):
                st.markdown(f"**🔹 Resumo:** {reply_cleaned}")

            if sources:
                st.markdown("### 🔗 **Fontes da Resposta:**")
                for i, source in enumerate(sources):
                    st.markdown(f"- [{source['title']}]({source['url']})")
            else:
                st.markdown("🔍 **Nenhuma fonte foi encontrada para esta resposta.**")
        else:
            st.error(f"❌ Erro na API Perplexity: {response.json()}")

# 4️⃣ Decision Make
with tabs[3]:
    st.header("🤖 Decision Make - Tomada de Decisão Automatizada")
    st.write("IA ajuda a decidir próximos passos estratégicos.")

    options = ["Ajustar Campanha", "Explorar Novos Mercados", "Melhorar Produto"]
    decision = st.selectbox("Qual ação tomar?", options)

    if st.button("Confirmar Ação"):
        st.success(f"Ação '{decision}' registrada com sucesso!")
