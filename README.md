# 📚 Workshop -  Recomendador de Livros - PrograMaria

O que vamos construir: Um sistema inteligente de recomendação de livros que utiliza IA para ajudar usuários a encontrar livros baseados em suas preferências. O sistema combina uma base de dados local do Goodreads com ferramentas de busca online para oferecer recomendações personalizadas.

## 🎯 Funcionalidades

- **Busca por gênero e número de páginas**: Encontre livros específicos baseados em critérios como gênero literário e extensão
- **Busca por título**: Procure informações detalhadas de livros específicos
- **Integração com Goodreads**: Acesso a dados atualizados através da API do Apify
- **Chat interativo**: Interface conversacional para fazer solicitações em linguagem natural
- **Filtragem inteligente**: Sistema que prioriza livros com melhores avaliações

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**: Linguagem principal do projeto
- **FastMCP**: Framework para criação de servidores MCP (Model Context Protocol)
- **LangChain**: Framework para desenvolvimento de aplicações com LLM
- **LangGraph**: Para criação de agentes conversacionais
- **OpenAI GPT**: Modelo de linguagem para processamento das solicitações
- **Pandas**: Manipulação e análise de dados
- **Apify Goodreads Scraper**: Integração com dados do Goodreads

## 📋 Pré-requisitos

### 1. Instalação do UV

O UV é um gerenciador de pacotes e ambientes virtuais Python ultra-rápido, escrito em Rust.

**Para instalar o UV:**

- **macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **Windows**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Documentação oficial**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### 2. Conta OpenAI e Chave API

Para utilizar o sistema de chat com IA, você precisará de uma chave da OpenAI.

**Passos para obter a chave:**

1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Vá para a seção "API Keys" no painel
4. Clique em "Create new secret key"
5. Copie e guarde a chave com segurança

**Documentação oficial**: [https://platform.openai.com/docs/quickstart](https://platform.openai.com/docs/quickstart)

### 3. Conta Apify (Opcional)

Para acessar dados atualizados do Goodreads, você pode criar uma conta gratuita na Apify.

**Passos para obter a chave da Apify:**

1. Acesse [apify.com](https://apify.com/)
2. Crie uma conta gratuita
3. Vá para "Settings" > "Integrations"
4. Copie sua API Token

**Sobre o Goodreads MCP da Apify**: [https://apify.com/runtime/goodreads-book-scraper](https://apify.com/runtime/goodreads-book-scraper)

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd recomendador_livros_programaria
```

### 2. Instale as dependências usando UV
```bash
uv sync
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
APIFY_API_KEY=sua_chave_apify_aqui_opcional
```

**⚠️ Importante**: Nunca compartilhe suas chaves API publicamente ou as commit no repositório.

### 4. Baixar o arquivo do GoodReads
Se você não recebeu o csv ao se inscrever no workshop, baixe-o deste link: [Kaggle - GoodReads 100k books](https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k/data)


## 📖 Como Usar

### 1. Executando o Buscador (buscador.py)

O arquivo [`buscador.py`](buscador.py) implementa um servidor MCP que fornece ferramentas de busca na base de dados local.

#### Funcionalidades do Buscador:

**🔍 Função `buscador(genero, numero_pg)`**
- **Propósito**: Busca livros por gênero e número de páginas
- **Parâmetros**:
  - `genero` (string): Nome do gênero em inglês (ex: "fiction", "romance", "mystery")
  - `numero_pg` (int): Número aproximado de páginas (busca ±20 páginas)
- **Retorno**: Lista com os 10 melhores livros encontrados
- **Filtros aplicados**:
  - Busca por gênero (case-insensitive)
  - Faixa de páginas (±20 páginas do valor especificado)
  - Se houver muitos resultados (>100), filtra apenas livros com rating >4.0
  - Ordena por rating decrescente

**📚 Função `buscar_por_nome(titulo)`**
- **Propósito**: Busca informações detalhadas de um livro específico
- **Parâmetros**:
  - `titulo` (string): Nome do livro em inglês
- **Retorno**: Informações completas do livro incluindo autor, descrição, rating, etc.

#### Executando o buscador diretamente:
```bash
uv run python buscador.py
```

### 2. Executando o Chat Interativo (chat.py)

O arquivo [`chat.py`](chat.py) implementa um agente conversacional que utiliza as ferramentas do buscador.

#### Como funciona o Chat:

**🤖 Inicialização do Agente**
1. **Carregamento de variáveis**: Lê as chaves API do arquivo `.env`
2. **Configuração do cliente MCP**: Conecta-se aos serviços:
   - `buscador_livros`: Servidor local com a base de dados
   - `apify`: Serviço externo para dados atualizados do Goodreads
3. **Inicialização do LLM**: Configura o modelo OpenAI GPT-4 mini
4. **Criação do agente**: Configura um agente ReAct (Reasoning + Acting) com:
   - Prompt em português especializado em recomendação de livros
   - Acesso às ferramentas de busca
   - Memória para manter contexto da conversa

**💬 Processo de Conversa**
1. **Input do usuário**: Sistema aceita solicitações em linguagem natural
2. **Processamento**: O agente analisa a solicitação e decide quais ferramentas usar
3. **Execução de ferramentas**: 
   - Traduz gêneros para inglês automaticamente
   - Classifica livros como "curtos" (≤130 páginas) ou "longos" (≥400 páginas)
   - Executa buscas na base local ou no Goodreads via Apify
4. **Resposta**: Retorna os 5 melhores livros baseados nas avaliações

#### Executando o chat:
```bash
uv run python chat.py
```

#### Exemplos de uso do chat:
```
> quero um romance curto
> preciso de um livro de ficção científica com mais de 300 páginas
> me recomende livros de mistério bem avaliados
> quero informações sobre o livro "1984"
> busque livros sobre programação
```

**Para sair do chat, digite:** `/q`

## 📊 Base de Dados

O projeto utiliza o arquivo `GoodReads_100k_books.csv` que contém informações de 100.000 livros do Goodreads com as seguintes colunas:

- **title**: Título do livro
- **author**: Autor(es)
- **pages**: Número de páginas
- **genre**: Gênero literário
- **rating**: Avaliação média (0-5)
- **desc**: Descrição/sinopse
- **bookformat**: Formato do livro
- **img**: URL da imagem da capa
- **isbn/isbn13**: Códigos ISBN
- **link**: Link para o Goodreads
- **reviews**: Número de reviews
- **totalratings**: Total de avaliações

## 🔧 Arquitetura do Sistema

```
recomendador_livros_programaria/
├── buscador.py          # Servidor MCP com ferramentas de busca
├── chat.py              # Interface conversacional
├── GoodReads_100k_books.csv  # Base de dados local
├── .env                 # Variáveis de ambiente (não versionado)
├── pyproject.toml       # Configuração do projeto e dependências
├── uv.lock             # Lock file das dependências
└── README.md           # Documentação (este arquivo)
```

### Fluxo de Dados:

1. **Usuário** → `chat.py` (interface conversacional)
2. **Chat** → **LangGraph Agent** (processamento da linguagem natural)
3. **Agent** → **MCP Tools** (ferramentas de busca)
4. **MCP Tools** → **Base Local** (`GoodReads_100k_books.csv`)
5. **MCP Tools** → **Apify Goodreads** (dados online atualizados)
6. **Resultados** → **Agent** → **Usuário** (recomendações formatadas)

## 🚨 Solução de Problemas

### Problemas Comuns:

**❌ Erro: "No module named 'openai'"**
- Solução: Execute `uv sync` para instalar as dependências

**❌ Erro: "Invalid API key"**
- Solução: Verifique se a chave OpenAI está correta no arquivo `.env`

**❌ Erro: "File not found: GoodReads_100k_books.csv"**
- Solução: Certifique-se de que o arquivo CSV está na raiz do projeto

**❌ Chat não responde ou trava**
- Solução: Verifique sua conexão com a internet e se as chaves API estão funcionando

### Debug:

Para debugar o sistema, você pode:

1. **Executar o buscador diretamente** para testar as ferramentas
2. **Verificar os logs** - o sistema usa logging para rastrear operações
3. **Testar as APIs** separadamente antes de usar o chat

## 📝 Licença

Este projeto é para fins educacionais e de demonstração.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se livre para:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Otimizar o código

## 📞 Suporte

Para dúvidas sobre o projeto:

1. Consulte esta documentação
2. Verifique os links de documentação oficial das tecnologias utilizadas
3. Teste os exemplos fornecidos passo a passo

---

**Desenvolvido para o Workshop da PrograMaria** 💜