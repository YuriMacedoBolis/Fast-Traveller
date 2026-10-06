# Arquitetura da Aplicação - fast Traveller

## 1. Visão Geral
A aplicação **fast Traveller** segue a arquitetura padrão em camadas do framework **Django** (MVT - Model-View-Template), estendida para suportar uma **API REST própria** (utilizando Django REST Framework) e consumo de **APIs REST externas** de geolocalização e pontos de interesse.

## 2. Camadas da Aplicação e Responsabilidades

* **Camada de Apresentação (Frontend / Templates):**
  * Responsável pela interface do usuário (UI/UX) responsiva, construída com HTML5, CSS3, JavaScript e Bootstrap/Tailwind.
  * Renderiza os formulários de entrada (destino, orçamento, tempo, categorias) e dashboards interativos para exibição dos roteiros e relatórios.

* **Camada de Aplicação e Negócio (Backend / Views & Controllers):**
  * Desenvolvida em **Python 3.x** e **Django**.
  * **Views do Django / Endpoints DRF:** Gerenciam as requisições HTTP, autenticação de sessão/tokens, validações de entrada e renderização de respostas (HTML ou JSON).
  * **Módulo de Integração Externa:** Serviço responsável por realizar chamadas HTTP seguras à API de terceiros (ex: Google Places API / TripAdvisor API), lidando com limites de requisição, timeouts e tratamento de erros.
  * **Módulo de Regras de Negócio:** Algoritmo que filtra e ordena as atrações com base no tempo disponível e orçamento do viajante.

* **Camada de Persistência e Dados (Models & Banco de Dados):**
  * **Django ORM:** Mapeia os objetos da aplicação para o banco de dados relacional.
  * **Banco de Dados Relacional:** SQLite em ambiente de desenvolvimento local e PostgreSQL (ou MySQL) no ambiente de produção hospedado.

## 3. Tecnologias Utilizadas
* **Linguagem Backend:** Python 3.x
* **Framework Web:** Django
* **API REST Framework:** Django REST Framework (DRF)
* **Banco de Dados:** PostgreSQL (Produção) / SQLite (Desenvolvimento)
* **Consumo de API Externa:** Biblioteca `requests` do Python
* **Hospedagem / Deploy (Fase 2):** Render / PythonAnywhere / Railway com suporte a HTTPS e variáveis de ambiente via `.env`

## 4. Fluxo de Dados
1. O **Viajante** insere os dados da viagem (destino, orçamento, tempo e categorias) na interface web.
2. A **View/Controller do Django** valida a requisição do usuário.
3. A aplicação aciona o **Módulo de Integração** que realiza uma requisição `GET` para a **API Externa de Locais** utilizando uma chave de API armazenada de forma segura nas variáveis de ambiente.
4. A **API Externa** retorna uma lista de atrações no formato JSON.
5. O **Módulo de Regras de Negócio** filtra as opções para que caibam no orçamento e tempo do usuário.
6. O **Django ORM** persiste o roteiro gerado no **Banco de Dados Relacional**.
7. O sistema retorna o roteiro montado na tela do usuário e disponibiliza o dado para consulta na **API REST própria** em `/api/v1/roteiros/`.