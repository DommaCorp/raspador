import streamlit as st
import google.generativeai as genai

# =====================================================================
# 1. CONFIGURAÇÃO DE SEGURANÇA E API (CÉREBRO AUTOMÁTICO)
# =====================================================================
try:
    chave_api = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=chave_api)
    
    # Procura o melhor modelo disponível automaticamente
    modelo_escolhido = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name:
                modelo_escolhido = m.name.replace('models/', '')
                break
    
    if not modelo_escolhido:
        modelo_escolhido = 'gemini-pro'

    modelo_ia = genai.GenerativeModel(modelo_escolhido)

except KeyError:
    st.error("⚠️ Chave de API não encontrada nos Secrets.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Erro ao ligar à Google: {e}")
    st.stop()

# =====================================================================
# 2. A TUA INSTRUÇÃO ESTRATÉGICA (O PROMPT)
# =====================================================================
# Agora pedimos um RELATÓRIO em vez de um código JSON
INSTRUCAO_IA = """
És um analista de mercado e copywriter especializado em e-commerce brasileiro.
Realiza uma pesquisa aprofundada com base no produto informado e nos links fornecidos. 
Aplica neurolinguística voltada para ativação do cérebro reptiliano (segurança, status, prazer, dor evitada, prova social). 

A tua missão é entregar um relatório estratégico completo e detalhado, formatado de forma visualmente agradável em Markdown. 
Usa títulos (##, ###), listas (*), negritos e emojis para facilitar a leitura.

O teu relatório DEVE conter as seguintes secções:

1. 📊 VISÃO GERAL DO MERCADO: Produto, preço médio estimado, nota geral e volume de avaliações.
2. 🗺️ MAPA COMPETITIVO: Principais concorrentes, os seus preços, diferenciais e falhas.
3. 🗣️ VOZ DO CLIENTE (Avaliações): Sentimento geral, maiores elogios e piores reclamações.
4. 🎯 PÚBLICO-ALVO E PERSONA: Perfil demográfico, psicográfico, frustrações e desejos profundos.
5. 🧠 NEUROLINGUÍSTICA E OBJEÇÕES: Palavras que ativam a compra, palavras a evitar e quebra das principais objeções.
6. 📈 ANÁLISE SWOT: Forças, Fraquezas, Oportunidades e Ameaças do produto e das avaliações.
7. 🔑 PALAVRAS-CHAVE SEO: Cria uma tabela ou lista com até 20 palavras-chave essenciais. Classifica-as como "Cauda Curta" ou "Cauda Longa" e organiza-as da mais barata para a mais cara em custo de anúncio.
8. ✍️ COPYWRITING: Uma sugestão de descrição otimizada para o Mercado Livre e 5 sugestões de títulos matadores.

Gera apenas o relatório final, sem introduções desnecessárias.
"""

# =====================================================================
# 3. INTERFACE VISUAL DA TUA APP (STREAMLIT)
# =====================================================================
st.set_page_config(page_title="O Raspador - Análise E-commerce", layout="wide")

st.title("🛒 O Raspador: Análise Neurolinguística E-commerce BR")

produto = st.text_input("📦 Nome do Produto (Obrigatório):", placeholder="Ex: Sérum Vitamina C Principia")

st.info("💡 **Fontes Sugeridas:** Mercado Livre, Amazon, Shopee, TikTok Shop, YouTube, Temu, Magalu, site oficial, etc.")
st.write("Introduz pelo menos 1 link de referência. Podes adicionar até 8 fontes para uma análise mais profunda.")

col1, col2 = st.columns(2)
with col1:
    link1 = st.text_input("🔗 Link 1 (Obrigatório):")
    link2 = st.text_input("🔗 Link 2 (Opcional):")
    link3 = st.text_input("🔗 Link 3 (Opcional):")
    link4 = st.text_input("🔗 Link 4 (Opcional):")
with col2:
    link5 = st.text_input("🔗 Link 5 (Opcional):")
    link6 = st.text_input("🔗 Link 6 (Opcional):")
    link7 = st.text_input("🔗 Link 7 (Opcional):")
    link8 = st.text_input("🔗 Link 8 (Opcional):")

if st.button("🧠 Gerar Análise Completa com IA", type="primary"):
    
    if produto and link1:
        st.caption(f"🔧 A usar o modelo automático: {modelo_escolhido}")
        
        with st.spinner("A analisar o mercado, a estruturar o relatório e a categorizar palavras-chave... (Isto pode demorar cerca de 1 minuto)"):
            try:
                # 1. Limpeza dos links vazios
                todos_os_links = [link1, link2, link3, link4, link5, link6, link7, link8]
                links_preenchidos = [link for link in todos_os_links if link != ""]
                
                # 2. Formata para texto
                texto_dos_links = "\n".join([f"{i+1}. {link}" for i, link in enumerate(links_preenchidos)])
                
                # 3. Executa a IA (Agora de forma simples, sem forçar JSON!)
                prompt_completo = f"{INSTRUCAO_IA}\n\nProduto: {produto}\nLinks Fornecidos:\n{texto_dos_links}"
                resposta = modelo_ia.generate_content(prompt_completo)
                
                # 4. Mostra o relatório lindo e formatado no ecrã!
                st.success(f"✅ Relatório estratégico concluído utilizando {len(links_preenchidos)} fonte(s)!")
                
                # Desenha uma caixa à volta do relatório para ficar mais elegante
                with st.container(border=True):
                    st.markdown(resposta.text)
                
            except Exception as erro:
                mensagem_erro = str(erro)
                if "429" in mensagem_erro or "quota" in mensagem_erro.lower():
                    st.error("⏳ A tua Chave de API atingiu o limite de consultas por minuto. Aguarda uns instantes e tenta novamente!")
                else:
                    st.error(f"❌ Ocorreu um erro ao comunicar com a IA: {erro}")
    else:
        st.warning("⚠️ Preenche o Nome do Produto e pelo menos o Link 1 para avançarmos.")
