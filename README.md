# RAG_Gemini
# Agente Gerador de Código com RAG & Embeddings

Este projeto é uma aplicação de Inteligência Artificial Generativa desenvolvida para transformar descrições em linguagem natural em código-fonte técnico e funcional. A implementação utiliza a técnica de **RAG (Retrieval-Augmented Generation)** com **Busca Vetorial**, garantindo que a IA consulte diretrizes de arquitetura, padrões de Clean Code e requisitos de QA antes de gerar a resposta.

## Funcionalidades

- **Geração Automática de Código:** Criação de scripts e funções baseadas em requisitos do usuário.
- **RAG com Embeddings:** Segmentação de documentos em *chunks* e busca semântica para maior precisão.
- **Toggle Comparativo:** Opção de ativar/desativar o contexto local para demonstrar o impacto do RAG.
- **Interface Web:** Desenvolvido com Streamlit para uma apresentação prática e visual.
- **Integração Gemini:** Utiliza o modelo `gemini-2.5-flash` (Geração) e `gemini-embedding-001` (Vetores).


## Pré-requisitos

- Python 3.10 ou superior.
- Uma API Key do Google Gemini (Obtenha gratuitamente no Google AI Studio).

# Instalação e Execução (Windows)

1. Crie o ambiente virtual:
```python -m venv venv```

2. Ative o ambiente virtual:
```.\venv\Scripts\activate```

3. Instale as dependências necessárias:
```pip install -r requirements.txt```

4. Colar a chave no arquivo .env
```CHAVE_API = SUA_CHAVE_API_AQUI```

5. Execute a aplicação:
```streamlit run man2.py```