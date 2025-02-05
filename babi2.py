import streamlit as st
import requests

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

# Criar Tabs de Navegação
tabs = st.tabs(["Configuração + Fontes", "Dashboard", "Data Lab", "Decision Make"])

# 1️⃣ Configuração + Fontes
with tabs[0]:
    st.header("🔧 Configuração e Fontes de Dados")
    st.write("Defina palavras-chave e fontes de coleta de dados para o monitoramento.")
    
    keywords = st.text_area("Palavras-chave para monitoramento", "inteligência artificial, mercado, inovação")
    if st.button("Salvar Configuração"):
        st.session_state.keywords = keywords
        st.success("Configuração salva com sucesso!")

# 2️⃣ Dashboard
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

# 3️⃣ Data Lab (Integração com Perplexity API)
with tabs[2]:
    st.header("🔬 Data Lab - Análise Semântica e IA")
    st.write("Análise semântica com InfraNodus e respostas da API Perplexity.")

    user_input = st.chat_input("Pergunte sobre as tendências do mercado...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Exibir input do usuário
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Enviar para a API da Perplexity
        payload = {
            "model": "sonar-reasoning-pro",
            "messages": st.session_state.messages
        }
        
        response = requests.post("https://api.perplexity.ai/chat/completions", headers=HEADERS, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            reply = response_data["choices"][0]["message"]["content"]
            sources = response_data.get("sources", [])  # Obtém as fontes

            st.session_state.messages.append({"role": "assistant", "content": reply})

            # Melhor apresentação da resposta
            with st.expander("💡 **Resposta da Perplexity**"):
                st.markdown(f"**🔹 Resumo:** {reply}")

            # Exibição de Fontes clicáveis
            if sources:
                st.markdown("### 🔗 **Fontes da Resposta:**")
                for i, source in enumerate(sources):
                    st.markdown(f"- [{source['title']}]({source['url']})")  # Fonte Clicável
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

