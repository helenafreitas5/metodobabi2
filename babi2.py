import streamlit as st
import requests
import json
import time

# Configuração da Página
st.set_page_config(page_title="Método Babi - Monitoramento IA", layout="wide")

# Carregar chave da API do Streamlit Secrets
API_KEY = st.secrets["perplexity"]["API_KEY"]
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Inicializar sessão de histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout principal
tabs = st.tabs(["Configuração + Fontes", "Dashboard", "Data Lab", "Decision Make"])

# Seção de Configuração + Fontes
with tabs[0]:
    st.header("🔧 Configuração e Fontes de Dados")
    st.write("Defina palavras-chave e fontes de coleta de dados para o monitoramento.")
    keywords = st.text_area("Palavras-chave para monitoramento", "inteligência artificial, mercado, inovação")
    if st.button("Salvar Configuração"):
        st.session_state.keywords = keywords
        st.success("Configuração salva com sucesso!")

# Seção de Dashboard
with tabs[1]:
    st.header("📊 Dashboard - Monitoramento de Notícias")
    st.write("Visualização das últimas notícias categorizadas pela IA.")
    
    # Simulação de notícias categorizadas
    example_news = [
        {"Data": "2025-02-05", "Link": "https://noticia1.com", "Relevância": "Bomba", "Resumo": "Nova tendência no mercado AI!",
         "Fortalezas": "Alto impacto", "Fraquezas": "Alto risco", "Público-alvo": "Empresas de tecnologia", "Colaboração": "Nenhuma", "Período da Ação": "Q1 2025"},
        {"Data": "2025-02-04", "Link": "https://noticia2.com", "Relevância": "BAU", "Resumo": "Concorrente lançou novo produto.",
         "Fortalezas": "Inovação incremental", "Fraquezas": "Pouca adoção inicial", "Público-alvo": "Startups", "Colaboração": "Parceria com X", "Período da Ação": "Q2 2025"}
    ]
    st.table(example_news)

# Seção de Data Lab (Análise Semântica)
with tabs[2]:
    st.header("🔬 Data Lab - Análise Semântica e IA")
    st.write("Análise semântica com InfraNodus e respostas da API Perplexity.")
    
    st.subheader("💬 Chat com a IA - Perplexity API")
    
    # Exibir histórico de mensagens com layout melhorado
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    user_input = st.chat_input("Digite sua pergunta...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Exibir indicador de carregamento
        with st.chat_message("assistant"):
            response_box = st.empty()
            response_box.markdown("⏳ Processando resposta...")
        
        payload = {
            "model": "sonar-reasoning-pro",
            "messages": st.session_state.messages,
            "include_sources": True  # Solicita fontes na resposta
        }
        response = requests.post("https://api.perplexity.ai/chat/completions", headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            reply = response_data["choices"][0]["message"]["content"]
            
            # Atualizar a resposta gradualmente
            response_text = ""
            for char in reply:
                response_text += char
                time.sleep(0.01)
                response_box.markdown(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Exibir fontes se houverem
            if "sources" in response_data["choices"][0]["message"]:
                sources = response_data["choices"][0]["message"]["sources"]
                st.markdown("🔗 **Fontes:**")
                for source in sources:
                    st.markdown(f"- [{source['title']}]({source['url']})")
        else:
            st.error(f"❌ Erro na API Perplexity: {response.json()}")

# Seção de Decision Make
with tabs[3]:
    st.header("🤖 Decision Make - Tomada de Decisão Automatizada")
    st.write("IA ajuda a decidir próximos passos estratégicos.")
    options = ["Ajustar Campanha", "Explorar Novos Mercados", "Melhorar Produto"]
    decision = st.selectbox("Qual ação tomar?", options)
    if st.button("Confirmar Ação"):
        st.success(f"Ação '{decision}' registrada com sucesso!")
