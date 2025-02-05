import streamlit as st
import requests
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Método Babi - Automação Inteligente", layout="wide")

# Barra de Navegação
menu = st.sidebar.radio("Navegação", ["Configuração + Fontes", "Dashboard", "Data Lab", "Decision Make"])

# 🟢 1️⃣ Configuração + Fontes
if menu == "Configuração + Fontes":
    st.header("📌 Configuração Inicial")
    frequencia = st.selectbox("Frequência de Análise:", ["Tempo Real", "Diária", "Semanal"])
    palavras_chave = st.text_input("Palavras-chave para monitoramento:")
    if st.button("Salvar Configuração"):
        st.success("✅ Configuração salva!")
    
    st.header("📡 Fontes de Dados")
    fontes = ["Google Alerts", "RSS Feeds", "LinkedIn", "Instagram", "TikTok"]
    selecionadas = st.multiselect("Selecione as fontes de monitoramento:", fontes, default=fontes)
    if st.button("🔄 Atualizar Dados"):
        st.success("Dados atualizados com sucesso!")

# 🔵 2️⃣ Dashboard
elif menu == "Dashboard":
    st.header("📊 Dashboard - Monitoramento e Estratégia")
    
    # Categorização das Notícias
    st.subheader("📰 Categorização Automática das Notícias")
    categorias = ["BAU (Business as Usual)", "Bomba (Impacto Alto)", "Ação Ninja (Movimento Estratégico)"]
    categoria_escolhida = st.radio("Escolha a categoria:", categorias)
    if st.button("Classificar Notícias"):
        st.success(f"✅ Notícias categorizadas como: {categoria_escolhida}")
    
    # Tabela de Monitoramento
    st.subheader("📅 Últimas Notícias Categorizadas")
    df = pd.DataFrame({
        "Data": ["2025-02-05", "2025-02-04"],
        "Link": ["https://noticia1.com", "https://noticia2.com"],
        "Relevância": ["Bomba", "BAU"],
        "Resumo (Tweet)": ["Nova tendência no mercado AI!", "Concorrente lançou novo produto."],
        "Fortalezas": ["Alto impacto", "Inovação incremental"],
        "Fraquezas": ["Alto risco", "Pouca adoção inicial"],
        "Público-alvo": ["Empresas de tecnologia", "Startups"],
        "Colaboração": ["Nenhuma", "Parceria com X"],
        "Período da Ação": ["Q1 2025", "Q2 2025"]
    })
    st.dataframe(df)
    
    # 🔵 Fase 4 e 5: Padrões e Monitoramento
    st.subheader("📈 Identificação de Padrões e Monitoramento Contínuo")
    st.write("Aqui serão exibidos padrões emergentes e mudanças nos territórios estratégicos detectados.")
    
# 🟠 3️⃣ Data Lab
elif menu == "Data Lab":
    st.header("🧪 Data Lab - Análise Semântica com InfraNodus")
    
    if st.button("🔍 Analisar com InfraNodus"):
        response = requests.get("https://api.infranodus.com/analysis", params={"query": palavras_chave})
        if response.status_code == 200:
            st.success("✅ Análise semântica concluída!")
            st.json(response.json())
        else:
            st.error("❌ Erro ao conectar com InfraNodus")

# 🟣 4️⃣ Decision Make
elif menu == "Decision Make":
    st.header("🧠 Tomada de Decisão Interativa")
    opcoes = ["Gerar insights estratégicos", "Priorizar categorização automática", "Ambos"]
    decisao = st.radio("Qual abordagem deseja seguir?", opcoes)
    if st.button("🚀 Enviar Decisão"):
        st.success(f"✅ Decisão enviada: {decisao}")
    
    st.header("📑 Geração de Relatórios e Ações")
    if st.button("📤 Enviar relatório por e-mail"):
        st.success("✅ Relatório enviado para metodobabi@gmail.com")
    
    # Chatbot com Zaia
    st.subheader("🤖 Chatbot Zaia")
    pergunta = st.text_input("Pergunte algo para Zaia:")
    if st.button("Enviar Pergunta"):
        response = "Zaia ainda está aprendendo! Em breve, terá respostas mais inteligentes."
        st.write(response)
    
    # Chat com API da Perplexity
    st.subheader("🗣️ Chat com Perplexity API")
    consulta = st.text_input("Faça uma consulta à Perplexity AI:")
    if st.button("Consultar Perplexity"):
        response = requests.get("https://api.perplexity.ai/query", params={"query": consulta})
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error("❌ Erro ao conectar com Perplexity API")
