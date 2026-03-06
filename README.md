# E-commerce Data Scraper Pipeline

Um pipeline completo em Python para monitoramento de preços do site [Books to Scrape](https://books.toscrape.com/).

O projeto executa três etapas principais:

1. **Coleta de Dados:** Utiliza Selenium com Chromium em modo headless e XPath para extrair informações dos livros (título, preço, categoria, avaliação e disponibilidade).
2. **Processamento:** Utiliza Pandas para limpar e tratar os dados brutos (conversão de preços para numérico, avaliações para estrelas, etc).
3. **Armazenamento:** Utiliza SQLAlchemy para persistir os dados processados em um banco de dados PostgreSQL.

## Tecnologias Utilizadas

- **Scraping:** Selenium, Chromium
- **Processamento:** Pandas
- **Armazenamento:** PostgreSQL, SQLAlchemy
- **Orquestração:** Docker, Docker Compose
- **Linguagem:** Python 3.12

---

## Como Executar o Projeto

A maneira mais fácil e recomendada de rodar o projeto é utilizando o Docker e o Docker Compose, pois ele já configura automaticamente o banco de dados PostgreSQL e as dependências do Selenium (Chromium).

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

### Executando com Docker Compose

1. Clone o repositório:

   ```bash
   git clone https://github.com/itasrocha/ecommerce-data-scraper.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd ecommerce-data-scraper
   ```

3. Suba os containers com o Docker Compose:
   ```bash
   docker-compose up --build
   ```

O Docker Compose irá:

- Iniciar um container com o banco de dados PostgreSQL (`postgres:16-alpine`), criando o usuário, senha e banco de testes.
- Construir a imagem da aplicação (instalando Python, Chromium, ChromeDriver e os pacotes necessários).
- Executar o pipeline completo inserindo os dados no Postgres.

Você verá os logs de execução do Selenium, do processo no Pandas e, finalmente, as estatísticas de armazenamento no banco de dados.

Para interromper os serviços, pressione `Ctrl+C` no terminal.

---

## Estrutura do Projeto

- `main.py`: Ponto de entrada que orquestra as três etapas da pipeline.
- `scraper.py`: Funções responsáveis por abrir o site com o Selenium e coletar os dados brutos usando XPath.
- `processor.py`: Funções responsáveis por formatar e limpar os dados importando-os para o Pandas.
- `storage.py`: Configurações e modelos do SQLAlchemy, lidando com a inserção e gestão de dados no PostgreSQL.
- `docker-compose.yml`: Configuração dos serviços (`db` e `scraper`) no Docker.
- `Dockerfile`: Configura a imagem da aplicação com Python e pacotes pro Selenium (Chromium).
