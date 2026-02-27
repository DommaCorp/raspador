import streamlit as st
import google.generativeai as genai
import json

# =====================================================================
# 1. CONFIGURAÇÃO DE SEGURANÇA E API
# =====================================================================
# O Streamlit vai procurar a chave secreta no servidor de forma segura
try:
    chave_api = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=chave_api)
    modelo_ia = genai.GenerativeModel('gemini-1.5-pro-latest')
except KeyError:
    st.error("⚠️ Chave de API não encontrada. Configura a GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# =====================================================================
# 2. A TUA INSTRUÇÃO ESTRATÉGICA (O CÉREBRO)
# =====================================================================
INSTRUCAO_IA = """
És um analista de mercado especializado em e-commerce brasileiro.
Realiza uma pesquisa aprofundada com base no produto informado e nos links fornecidos. 
Aplica neurolinguística voltada para ativação do cérebro reptiliano (segurança, status, prazer, dor evitada, prova social). 
Entregar análise estratégica completa orientada para conversão em marketplaces.

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
  "descricao_otimizada_mercado_livre": "",
  "titulos_sugeridos": []
}
"""

# =====================================================================
# 3. INTERFACE VISUAL DA TUA APP (STREAMLIT)
# =====================================================================
st.set_page_config(page_title="O Raspador - Análise E-commerce", layout="wide")

st.title("🛒 O Raspador: Análise Neurolinguística E-commerce BR")
st.write("Introduz o nome do produto e no mínimo 3 links de marketplaces para gerar a tua estratégia.")

# Cria as caixas de texto para o utilizador preencher
col1, col2 = st.columns(2)
with col1:
    produto = st.text_input("📦 Nome do Produto (Ex: Sérum Vitamina C Principia):")
    link1 = st.text_input("🔗 Link 1 (Mercado Livre, Amazon, etc.):")
with col2:
    link2 = st.text_input("🔗 Link 2:")
    link3 = st.text_input("🔗 Link 3:")

# Botão principal
if st.button("🧠 Gerar Análise Completa com IA", type="primary"):
    
    # Validação: Verifica se preencheu o produto e os 3 links
    if produto and link1 and link2 and link3:
        
        with st.spinner("A analisar o mercado e a aplicar neurolinguística... (isto pode demorar 30 a 60 segundos)"):
            try:
                # Junta tudo para enviar à IA
                prompt_completo = f"{INSTRUCAO_IA}\n\nProduto: {produto}\nLinks:\n1. {link1}\n2. {link2}\n3. {link3}"
                
                # Pede a resposta à IA
                resposta = modelo_ia.generate_content(prompt_completo)
                
                # Limpa e formata o resultado
                texto_limpo = resposta.text.replace('```json', '').replace('```', '').strip()
                dados_json = json.loads(texto_limpo)
                
                st.success("✅ Análise estratégica concluída com sucesso!")
                
                # Mostra o resultado final bonito na tela!
                st.json(dados_json)
                
            except json.JSONDecodeError:
                st.error("A IA não retornou um formato de dados válido. Aqui está a resposta em texto bruto:")
                st.write(resposta.text)
            except Exception as erro:
                st.error(f"Ocorreu um erro no servidor: {erro}")
    else:

        st.warning("⚠️ Atenção: Precisas de preencher o nome do produto e os 3 links para a IA funcionar corretamente.")
