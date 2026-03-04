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
# Prompt atualizado com Neuromarketing Avançado, Arquétipos e restrições de Copy!
INSTRUCAO_IA = """
És um analista de mercado, especialista em neuromarketing e copywriter de e-commerce brasileiro.
Realiza uma pesquisa aprofundada com base no produto informado e nos links fornecidos. 

A tua missão é entregar um relatório estratégico completo, formatado de forma visualmente agradável em Markdown. 
Podes usar emojis nos títulos das secções para organizar o relatório, MAS NUNCA uses emojis na secção de COPYWRITING.

O teu relatório DEVE conter as seguintes secções:

1. 📊 VISÃO GERAL DO MERCADO: Produto, preço médio estimado, nota geral e volume de avaliações.
2. 🗺️ MAPA COMPETITIVO: Principais concorrentes, os seus preços, diferenciais e falhas.
3. 🗣️ VOZ DO CLIENTE (Avaliações): Sentimento geral, maiores elogios e piores reclamações.
4. 🎯 PÚBLICO-ALVO, PERSONA E ARQUÉTIPO: Perfil demográfico, psicográfico, frustrações e desejos profundos. Identifica o ARQUÉTIPO DO COMPRADOR principal e explica o seu padrão de comportamento.
5. 🧠 NEURO VENDAS E OBJEÇÕES: Usa o Arquétipo identificado para aplicar uma estrutura de neuro venda. Explica como vender diretamente para o cérebro reptiliano deste comprador (segurança, status, prazer, dor evitada). Inclui palavras que ativam a compra e a quebra das principais objeções.
6. 📈 ANÁLISE SWOT: Forças, Fraquezas, Oportunidades e Ameaças do produto.
7. 🔑 PALAVRAS-CHAVE E BRANDING ADS: 
   - SEO / Fundo de Funil: Tabela com até 20 palavras-chave essenciais, classificadas como "Cauda Curta" ou "Cauda Longa". Organiza-as em ordem crescente de custo usando APENAS os termos: "Custo Baixo", "Custo Médio", "Custo Alto" ou "Custo Muito Alto" (não uses valores monetários).
   - Branding Ads / Topo de Funil: Lista de palavras e termos recomendados para usar em campanhas de reconhecimento de marca.
8. ✍️ COPYWRITING: 
   - Descrição (Copy): Cria uma descrição otimizada, focada em conversão. REGRA ESTRITA: NÃO uses emojis nesta descrição.
   - Títulos Matadores: 5 sugestões de títulos criativos focados em conversão.
   - Títulos Estruturados (SEO): Fornece mais 5 sugestões de títulos baseados nas palavras-chave da busca, seguindo RIGOROSAMENTE a seguinte fórmula estrutural: "Produto + Marca + Linha ou Modelo + Caracteristica Principal + Variação relevante".
   - REGRAS ESTRITAS PARA TODOS OS TÍTULOS: Cada título deve ter NO MÁXIMO 60 caracteres. NÃO uses emojis. É ESTRITAMENTE PROIBIDO usar as palavras "Full", "brinde", "promoção", "ultimas unidades", "acabando" ou quaisquer sinónimos de escassez barata.

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
        
        with st.spinner("A analisar arquétipos, neuro vendas e a estruturar o relatório... (Isto pode demorar cerca de 1 minuto)"):
            try:
                # 1. Limpeza dos links vazios
                todos_os_links = [link1, link2, link3, link4, link5, link6, link7, link8]
                links_preenchidos = [link for link in todos_os_links if link != ""]
                
                # 2. Formata para texto
                texto_dos_links = "\n".join([f"{i+1}. {link}" for i, link in enumerate(links_preenchidos)])
                
                # 3. Executa a IA
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
