import streamlit as st
import requests
import re  # Biblioteca para remover padrões de texto

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

            # 🔹 **Remover qualquer "<think>" da resposta**
            reply_cleaned = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()

            st.session_state.messages.append({"role": "assistant", "content": reply_cleaned})

            # Melhor apresentação da resposta
            with st.expander("💡 **Resposta da Perplexity**"):
                st.markdown(f"**🔹 Resumo:** {reply_cleaned}")

            # Exibição de Fontes clicáveis
            if sources:
                st.markdown("### 🔗 **Fontes da Resposta:**")
                for i, source in enumerate(sources):
                    st.markdown(f"- [{source['title']}]({source['url']})")  # Fonte Clicável
            else:
                st.markdown("🔍 **Nenhuma fonte foi encontrada para esta resposta.**")
        else:
            st.error(f"❌ Erro na API Perplexity: {response.json()}")
