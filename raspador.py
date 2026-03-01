import streamlit as st
import google.generativeai as genai
import json

# =====================================================================
# 1. CONFIGURAÇÃO DE SEGURANÇA E API
# =====================================================================
try:
    chave_api = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=chave_api)
    
    # MUITO IMPORTANTE: Usar o modelo Flash, que tem limites muito maiores!
    modelo_ia = genai.GenerativeModel('gemini-2.0-flash')
except KeyError:
    st.error("⚠️ Chave de API não encontrada nos Secrets.")
    st.stop()

# =====================================================================
# 2. A TUA INSTRUÇÃO ESTRATÉGICA (O CÉREBRO)
# =====================================================================
# Adicionei a regra das 20 palavras-chave e a nova estrutura JSON no final
INSTRUCAO_IA = """
És um analista de mercado especializado em e-commerce brasileiro.
Realiza uma pesquisa aprofundada com base no produto informado e nos links fornecidos. 
Aplica neurolinguística voltada para ativação do cérebro reptiliano (segurança, status, prazer, dor evitada, prova social). 
Entregar análise estratégica completa orientada para conversão em marketplaces.

REGRAS PARA PALAVRAS-CHAVE:
Gera uma lista de até 20 palavras-chave. Se não existirem 20, gera as que encontrares.
Classifica cada uma como "cauda curta" (ampla) ou "cauda longa" (específica).
Organiza a lista OBRIGATORIAMENTE em ordem crescente de custo de anúncio (da palavra mais barata para a mais cara).

DEVES RESPONDER EXCLUSIVAMENTE NO FORMATO JSON ABAIXO, SEM NENHUM TEXTO ANTES OU DEPOIS. 
Preenche todos os campos vazios com a tua análise:

{
  "analise_mercado": {
    "titulo": "ANÁLISE DE MERCADO",
    "produto_analisado": "",
    "preco_estimado": "",
    "nota_e_avaliacoes": "",
    "mapa_competitivo": {
      "concorrentes_diretos": [],
      "precos_concorrentes": [],
      "avaliacoes": [],
      "notas": [],
      "diferenciais": [],
      "apelo_principal": [],
      "volume_vendas_estimado": []
    },
    "observacoes_mapa_competitivo": ""
  },
  "analise_avaliacoes": {
    "volume_total": "",
    "distribuicao_sentimento": {"positivo": "", "neutro_negativo": ""},
    "palavras_mais_usadas": [],
    "elogios_recorrentes": {"efeito_imediato": "", "qualidade_eficacia": "", "sensorial": "", "fidelidade_marca": "", "confianca": "", "experiencia_compra": ""},
    "reclamacoes_recorrentes": {"preco": "", "cheiro": "", "falsificacao": ""}
  },
  "posicionamento_atual": {
    "como_esta_sendo_vendido": "",
    "principal_apelo": "",
    "o_que_funciona": "",
    "o_que_pode_melhorar": {"visibilidade_alcance": "", "comunicacao_custo_beneficio": "", "abordagem_preocupacoes": "", "conteudo_visual_descritivo": {"imagens": "", "videos": "", "informacoes_detalhadas": ""}, "estrategias_marketing_digital": ""}
  },
  "analise_swot": {
    "produto": {"forcas": [], "fraquezas": [], "oportunidades": [], "ameacas": []},
    "avaliacoes": {"forcas": [], "fraquezas": [], "oportunidades": [], "ameacas": []}
  },
  "diferencial_unico_uvp": "",
  "persona_principal": "",
  "mapa_demografico": "",
  "mapa_psicografico": {"frustracoes": [], "medos": [], "aspiracoes": [], "comportamento_compra": []},
  "arquetipo_comprador": "",
  "jornada_cliente_5_estagios": [],
  "publico_alvo_detalhado": {
    "perfil_demografico": {"genero": "", "idade": "", "renda": "", "localizacao": "", "educacao": ""},
    "perfil_psicografico": {"estilo_vida": "", "valores": "", "interesses": "", "comportamento_compra": ""},
    "dores_necessidades_resolvidas": ""
  },
  "analise_linguagem_avaliacoes": {"palavras_que_convertem": [], "palavras_a_evitar": []},
  "objecoes_principais": [],
  "palavras_chave_seo": [
    {
      "palavra": "",
      "tipo": "cauda curta ou cauda longa",
      "ordem_custo": "1 (mais barata) a 20 (mais cara)"
    }
  ],
  "descricao_otimizada_mercado_livre": "",
  "titulos_sugeridos": []
}
"""

# =====================================================================
# 3. INTERFACE VISUAL DA TUA APP (STREAMLIT)
# =====================================================================
st.set_page_config(page_title="O Raspador - Análise E-commerce", layout="wide")

st.title("🛒 O Raspador: Análise Neurolinguística E-commerce BR")

# Campo do produto em destaque
produto = st.text_input("📦 Nome do Produto (Obrigatório):", placeholder="Ex: Sérum Vitamina C Principia")

# Sugestões de fontes
st.info("💡 **Fontes Sugeridas:** Podes colar links do Mercado Livre, Amazon, Shopee, TikTok Shop, YouTube, Temu, Magalu, site oficial, etc.")
st.write("Introduz pelo menos 1 link de referência. Podes adicionar até 8 fontes para uma análise mais profunda.")

# Organização dos 8 campos em 2 colunas
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
    
    # Validação: Agora só exige o Produto e o Link 1
    if produto and link1:
        with st.spinner("A analisar o mercado e a categorizar palavras-chave..."):
            try:
                # 1. Limpeza dos links: Guarda apenas os que o utilizador preencheu
                todos_os_links = [link1, link2, link3, link4, link5, link6, link7, link8]
                links_preenchidos = [link for link in todos_os_links if link != ""]
                
                # 2. Formata os links preenchidos como uma lista de texto (1. link..., 2. link...)
                texto_dos_links = "\n".join([f"{i+1}. {link}" for i, link in enumerate(links_preenchidos)])
                
                # 3. Junta tudo no prompt
                prompt_completo = f"{INSTRUCAO_IA}\n\nProduto: {produto}\nLinks Fornecidos:\n{texto_dos_links}"
                
                # Pede a resposta à IA
                resposta = modelo_ia.generate_content(prompt_completo)
                
                # Limpa a resposta
                texto_limpo = resposta.text.replace('```json', '').replace('```', '').strip()
                dados_json = json.loads(texto_limpo)
                
                st.success(f"✅ Análise estratégica concluída utilizando {len(links_preenchidos)} fonte(s)!")
                st.json(dados_json)
                
            except json.JSONDecodeError:
                st.error("A IA não retornou um formato JSON válido. Resposta bruta:")
                st.write(resposta.text)
            except Exception as erro:
                mensagem_erro = str(erro)
                if "429" in mensagem_erro or "quota" in mensagem_erro.lower():
                    st.error("⏳ A tua Chave de API ainda está bloqueada por limite de quota. Confirma no Google AI Studio se o plano 'Pay-as-you-go' já está ativo e se criaste uma chave nova!")
                else:
                    st.error(f"❌ Ocorreu um erro no servidor: {erro}")
    else:
        # Novo aviso amigável
        st.warning("⚠️ Preenche o Nome do Produto e pelo menos o Link 1 para avançarmos.")

