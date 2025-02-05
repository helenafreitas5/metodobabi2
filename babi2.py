import streamlit as st
import requests
import json

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

# 🔧 Seção de Configuração + Fontes
with tabs[0]:
    st.header("🔧 Configuração e Fontes de Dados")
    st.write("Defina palavras-chave e fontes de coleta de dados para o monitoramento.")
    keywords = st.text_area("Palavras-chave para monitoramento", "inteligência artificial, mercado, inovação")
    if st.button("Salvar Configuração"):
        st.session_state.keywords = keywords
        st.success("Configuração salva com sucesso!")

# 📊 Seção de Dashboard - Monitoramento de Notícias
with tabs[1]:
    st.header("📊 Dashboard - Monitoramento de Notícias")
    st.write("Visualização das últimas notícias categorizadas pela IA.")

    # Simulação de notícias categorizadas
    example_news = [
        {
            "Data": "2025-02-05",
            "Título": "Grupo Boticário projeta crescimento ambicioso",
            "Resumo": "O Grupo Boticário pretende expandir a produção em 50% até 2028, investindo R$ 4,2 bi.",
            "Fonte": "https://noticia1.com"
        },
        {
            "Data": "2025-02-04",
            "Título": "Lançamento da linha 'Extinto' para sustentabilidade",
            "Resumo": "Nova linha de fragrâncias com logística reversa e sustentabilidade.",
            "Fonte": "https://noticia2.com"
        }
    ]

    for news in example_news:
        with st.container():
            st.markdown(f"### 📰 {news['Título']}")
            st.write(news["Resumo"])
            st.markdown(f"[🔗 Leia mais]({news['Fonte']})", unsafe_allow_html=True)
            st.divider()

# 🔬 Seção de Data Lab - Integração com Perplexity API
with tabs[2]:
    st.header("🔬 Data Lab - Insights via Perplexity AI")
    st.write("Faça perguntas e descubra insights estratégicos.")

    user_input = st.text_input("🔎 Digite sua pergunta sobre tendências de mercado...")
    
    if st.button("🔍 Consultar Perplexity"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Enviar requisição para Perplexity API
            payload = {
                "model": "sonar-reasoning-pro",
                "messages": st.session_state.messages,
                "include_sources": True  # Adiciona fontes na resposta
            }
            response = requests.post("https://api.perplexity.ai/chat/completions", headers=HEADERS, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                message = response_data["choices"][0]["message"]

                if "content" in message:
                    reply = message["content"]
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    with st.chat_message("assistant"):
                        st.markdown(reply)

                # 🔗 Exibir fontes como cartões interativos
                if "sources" in message and message["sources"]:
                    st.markdown("## 🔗 Fontes Utilizadas")
                    cols = st.columns(len(message["sources"]))

                    for i, source in enumerate(message["sources"]):
                        with cols[i]:
                            st.markdown(
                                f"""
                                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 10px; text-align: center;">
                                    <p><strong>{source['title']}</strong></p>
                                    <a href="{source['url']}" target="_blank">🔗 Acessar Fonte</a>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
            else:
                st.error(f"❌ Erro na API Perplexity: {response.json()}")

# 🤖 Seção de Decision Make
with tabs[3]:
    st.header("🤖 Decision Make - Tomada de Decisão Automatizada")
    st.write("IA ajuda a decidir próximos passos estratégicos.")
    options = ["Ajustar Campanha", "Explorar Novos Mercados", "Melhorar Produto"]
    decision = st.selectbox("Qual ação tomar?", options)
    if st.button("Confirmar Ação"):
        st.success(f"Ação '{decision}' registrada com sucesso!")
