import streamlit as st
import numpy as np
import os
from google import genai
from google.genai import types

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador RAG Pro", layout="wide")
st.title("🚀 Gerador de Código: RAG com Embeddings")

# --- FUNÇÕES TÉCNICAS (O CORAÇÃO DO RAG) ---

def gerar_chunks(texto, tamanho=600):
    """Quebra o manual de boas práticas em pedaços menores (Chunks)."""
    # Quebramos por parágrafos para não perder o contexto das frases
    chunks = [c.strip() for c in texto.split('\n\n') if len(c.strip()) > 10]
    return chunks

def buscar_contexto_similar(client, pergunta, chunks):
    """
    Aqui acontece a 'Mágica' do RAG:
    1. Transforma a pergunta em vetores.
    2. Transforma cada chunk em vetores.
    3. Compara quais chunks estão 'perto' da pergunta.
    """
    # Modelo de embedding estável
    MODELO_EMBED = "gemini-embedding-001" 

    # Gerando embedding da pergunta
    res_pergunta = client.models.embed_content(
        model=MODELO_EMBED,
        contents=pergunta
    )
    v_pergunta = np.array(res_pergunta.embeddings[0].values)

    # Gerando embeddings dos chunks
    res_chunks = client.models.embed_content(
        model=MODELO_EMBED,
        contents=chunks
    )
    v_chunks = [np.array(e.values) for e in res_chunks.embeddings]

    # Cálculo de Similaridade (Produto Escalar entre vetores)
    scores = [np.dot(v_pergunta, v_chunk) for v_chunk in v_chunks]
    
    # Seleciona os 2 chunks mais relevantes
    indices_top = np.argsort(scores)[-2:][::-1]
    return "\n\n".join([chunks[i] for i in indices_top])

# --- INTERFACE STREAMLIT ---

with st.sidebar:
    st.header("Painel de Controle")
    api_key = "AIzaSyCuWoAZ5Q3-dzHsg2ByP0aAu-l8EgHMU8I"
    usar_rag = st.toggle("Ativar Busca Vetorial (RAG)", value=True)
    st.divider()
    st.write("**Técnica:** Embeddings + Cosine Similarity")

requisito = st.text_area("Descreva o código que você precisa:", placeholder="Ex: Crie um sistema de login...")

if st.button("Gerar Código"):
    if not api_key:
        st.error("Insira a API Key para continuar.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            if usar_rag:
                # 1. Recuperação (Retrieval)
                if not os.path.exists("conhecimento/diretrizes.txt"):
                    st.error("Arquivo de diretrizes não encontrado na pasta 'conhecimento'!")
                    st.stop()
                
                with open("conhecimento/diretrizes.txt", "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                chunks = gerar_chunks(conteudo)
                
                with st.spinner("Calculando vetores e buscando contexto..."):
                    contexto_recuperado = buscar_contexto_similar(client, requisito, chunks)
                
                # 2. Aumentação (Augmentation)
                prompt_final = f"""
                Você é um Engenheiro de Software Sênior que so programa em python.
                Caso seja pedido para gerar codigo em outro idioma, responda que só programa em python e pergunte se deseja o código em python.
                Sempre de uma resposta curta e objetiva, sem rodeios. Se a pergunta for sobre um código específico, gere apenas o código solicitado, sem explicações ou comentários.
                Use o GUIA DE BOAS PRÁTICAS abaixo para basear sua resposta.
                Use este CONTEXTO ESPECÍFICO para gerar o código:
                {contexto_recuperado}
                
                REQUISITO: {requisito}
                Responda apenas com o código.
                """
                st.success("Contexto relevante encontrado via Embedding!")
                with st.expander("Ver Chunks recuperados"):
                    st.write(contexto_recuperado)
            else:
                prompt_final = requisito

            # 3. Geração (Generation)
            with st.spinner("IA Gerando código..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_final
                )
                st.subheader("💻 Código Final")
                st.code(response.text, language='python')

        except Exception as e:
            st.error(f"Erro técnico: {e}")