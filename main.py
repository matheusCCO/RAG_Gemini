import os
from dotenv import load_dotenv
import time
from google import genai
from google.genai import types

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÃO ---

NOME_ARQUIVO_CONTEXTO = "boas_praticas_python.txt"
MODELO = "gemini-2.5-flash" # Atualizado para a versão 2.5

client = genai.Client(api_key=os.getenv("CHAVE_API"))

def carregar_contexto():
    """Busca o conhecimento local (R em RAG)."""
    if not os.path.exists(NOME_ARQUIVO_CONTEXTO):
        # Caso o arquivo não exista, criamos um básico para não dar erro
        with open(NOME_ARQUIVO_CONTEXTO, "w", encoding="utf-8") as f:
            f.write("1. Use sempre Type Hints.\n2. Siga a PEP8.\n3. Escreva docstrings em português.")
    
    with open(NOME_ARQUIVO_CONTEXTO, "r", encoding="utf-8") as f:
        return f.read()

def agente_dev_rag():
    print(f" Iniciando Agente Dev (Modelo: {MODELO})")
    
    contexto = carregar_contexto()
    pergunta = input("\nDescreva o código que você precisa: ")

    if not pergunta.strip(): return

    # Prompt Aumentado (Augmented)
    prompt_completo = f"""
    Você é um Engenheiro de Software Sênior que so programa em python.
    Caso seja pedido para gerar codigo em outro idioma, responda que só programa em python e pergunte se deseja o código em python.
    Sempre de uma resposta curta e objetiva, sem rodeios. Se a pergunta for sobre um código específico, gere apenas o código solicitado, sem explicações ou comentários.
    Use o GUIA DE BOAS PRÁTICAS abaixo para basear sua resposta.
    
    --- GUIA DE BOAS PRÁTICAS ---
    {contexto}
    
    --- TAREFA DO USUÁRIO ---
    {pergunta}
    
    Responda apenas com o código.
    """

    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt_completo
        )

        print("\n" + "—"*50)
        print(" RESPOSTA GERADA COM SUCESSO:")
        print("—"*50)
        print(response.text)
        print("—"*50)

    except Exception as e:
        if "429" in str(e):
            print(" Erro: Limite de cota atingido (429). Aguarde 1 minuto.")
        else:
            print(f" Erro inesperado: {e}")

if __name__ == "__main__":
    agente_dev_rag()