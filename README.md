# fast Traveller

**Instituição:** Centro Universitário de Brasília

**Curso:** Ciência da Computação

**Disciplina:** Desenvolvimento Web

**Turma / Semestre:** 2026.2

**Professor(a):** Felipe Pires

**Status do projeto:** Protótipo / Em desenvolvimento — Entrega 1 Concluída

---

## Sumário

1. [Descrição do projeto](#1-descrição-do-projeto)
2. [Funcionalidades](#2-funcionalidades)
3. [Demonstração](#3-demonstração)
4. [Tecnologias utilizadas](#4-tecnologias-utilizadas)
5. [Arquitetura](#5-arquitetura)
6. [Organização dos diretórios](#6-organização-dos-diretórios)
7. [Participantes](#7-participantes)
8. [Como executar](#8-como-executar)
9. [Configuração](#9-configuração)
10. [Testes](#10-testes)
11. [Uso de inteligência artificial](#11-uso-de-inteligência-artificial)
12. [Contribuição e fluxo de trabalho](#12-contribuição-e-fluxo-de-trabalho)
13. [Histórico de versões](#13-histórico-de-versões)
14. [Limitações e próximos passos](#14-limitações-e-próximos-passos)
15. [Licença, referências e contato](#15-licença-referências-e-contato)

---

## 1. Descrição do projeto

O **fast Traveller** é uma aplicação web voltada para o planejamento ágil e personalizado de viagens.

A plataforma tem como objetivo ajudar viajantes a organizar seus roteiros considerando informações como:

* Destino;
* Duração da viagem;
* Orçamento disponível;
* Tempo disponível;
* Categorias de interesse.

A proposta é centralizar essas informações em uma única aplicação, permitindo que o usuário encontre opções de atrações e monte seu próprio roteiro de viagem de maneira mais prática.

O sistema utilizará uma integração com uma API externa de localização e pontos de interesse para obter informações sobre locais reais existentes no destino escolhido.

Além disso, a aplicação realizará cálculos relacionados ao orçamento da viagem, permitindo acompanhar o custo estimado das atrações selecionadas e o saldo disponível.

### Objetivo geral

Desenvolver uma plataforma web para planejamento e organização de roteiros de viagem personalizados, considerando o destino, o tempo disponível, os interesses do usuário e seu orçamento.

### Objetivos específicos

* Permitir o cadastro e a autenticação de usuários.
* Permitir o cadastro e gerenciamento de viagens.
* Capturar os parâmetros da viagem, como destino, duração, orçamento e interesses.
* Consultar pontos de interesse reais por meio de uma API externa.
* Permitir que o usuário selecione atrações para seu roteiro.
* Organizar as atrações selecionadas de acordo com a viagem.
* Calcular o custo estimado do roteiro.
* Apresentar o saldo restante do orçamento.
* Exibir informações consolidadas sobre os gastos da viagem.

### Público-alvo

O sistema é destinado principalmente a:

* Viajantes autônomos;
* Pessoas que realizam viagens curtas;
* Pessoas que viajam sozinhas;
* Turistas que desejam organizar seu roteiro de forma prática;
* Usuários que desejam controlar os gastos durante o planejamento da viagem.

---

## 2. Funcionalidades

| Funcionalidade                        | Descrição                                              | Status             |
| :------------------------------------ | :----------------------------------------------------- | :----------------- |
| **Autenticação de usuário**           | Cadastro, login e encerramento de sessão               | Planejada — Fase 2 |
| **Gestão de viagens**                 | Criação, consulta, atualização e exclusão de viagens   | Planejada — Fase 2 |
| **Cadastro dos parâmetros da viagem** | Destino, duração, orçamento e interesses               | Planejada — Fase 2 |
| **Integração com API externa**        | Consulta de pontos de interesse no destino             | Planejada — Fase 2 |
| **Busca de atrações**                 | Busca de locais de acordo com as categorias escolhidas | Planejada — Fase 2 |
| **Montagem do roteiro**               | Seleção e organização das atrações                     | Planejada — Fase 2 |
| **Controle de orçamento**             | Cálculo do custo estimado e saldo disponível           | Planejada — Fase 2 |
| **Relatório financeiro**              | Resumo dos gastos da viagem por categoria              | Planejada — Fase 2 |

### Requisitos não funcionais

#### Desempenho

* A API própria deverá responder às requisições comuns em até aproximadamente 2 segundos.
* Requisições à API externa deverão possuir timeout de até 5 segundos.
* O sistema deverá utilizar cache quando aplicável para reduzir requisições repetidas.

#### Segurança

* Senhas deverão ser armazenadas utilizando os mecanismos de hash fornecidos pelo Django.
* Credenciais e chaves de APIs deverão ser armazenadas em variáveis de ambiente.
* A chave da API externa não deverá ser exposta no frontend.
* Rotas privadas deverão exigir autenticação.

#### Usabilidade

* A interface deverá ser responsiva.
* O sistema deverá ser utilizável em computadores, tablets e dispositivos móveis.
* Os principais fluxos deverão possuir navegação simples e objetiva.

#### Disponibilidade

* O sistema deverá funcionar em ambiente local para desenvolvimento e testes.
* A aplicação poderá posteriormente ser implantada em ambiente de nuvem/PaaS.

---

## 3. Demonstração

Os protótipos e materiais visuais do projeto estão armazenados no diretório:

```text
docs/prototipos/
```

### Principais telas previstas

| Tela                      | Descrição                                                 |
| :------------------------ | :-------------------------------------------------------- |
| **Login e Cadastro**      | Permite autenticação e criação de uma conta               |
| **Dashboard**             | Apresenta as viagens cadastradas pelo usuário             |
| **Nova Viagem**           | Permite informar destino, duração, orçamento e interesses |
| **Sugestões de Atrações** | Apresenta locais encontrados para o destino               |
| **Montagem do Roteiro**   | Permite selecionar e organizar atrações                   |
| **Relatório**             | Apresenta custos estimados e saldo restante               |

### Protótipos

Os protótipos e especificações visuais podem ser consultados em:

[`docs/prototipos/`](docs/prototipos/)

---

## 4. Tecnologias utilizadas

| Camada                               | Tecnologia               | Versão                    |
| :----------------------------------- | :----------------------- | :------------------------ |
| **Linguagem**                        | Python                   | 3.11+                     |
| **Frontend**                         | HTML5, CSS3 e JavaScript | —                         |
| **Templates**                        | Django Templates         | Django 5.x                |
| **Framework Backend**                | Django                   | 5.x                       |
| **API REST**                         | Django REST Framework    | Compatível com Django 5.x |
| **Banco de dados — desenvolvimento** | SQLite                   | 3.x                       |
| **Banco de dados — produção**        | PostgreSQL               | 16+                       |
| **API externa**                      | Google Places API        | Conforme versão utilizada |
| **Controle de versão**               | Git                      | —                         |
| **Repositório**                      | GitHub                   | —                         |
| **Editor**                           | Visual Studio Code       | —                         |
| **Prototipação**                     | Figma / draw.io          | —                         |
| **Hospedagem planejada**             | Render                   | —                         |

---

## 5. Arquitetura

O **fast Traveller** utiliza o padrão arquitetural **MTV (Model-Template-View)** fornecido pelo Django, juntamente com uma camada de API REST desenvolvida utilizando o Django REST Framework.

A aplicação é organizada em camadas, permitindo separar a apresentação, as regras de negócio, o acesso aos dados e as integrações externas.

### Visão geral

```text
┌──────────────────────────┐
│          Usuário         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        Frontend          │
│ HTML / CSS / JavaScript  │
│    Django Templates      │
└────────────┬─────────────┘
             │
             │ HTTP / JSON
             ▼
┌──────────────────────────┐
│     Django Backend       │
│                          │
│ Django + Django REST     │
│ Framework                │
└──────┬───────────┬───────┘
       │           │
       │           │
       ▼           ▼
┌────────────┐ ┌─────────────────┐
│  Banco de  │ │  API Externa    │
│   Dados    │ │ Google Places    │
│            │ │      API         │
└────────────┘ └─────────────────┘
       │
       ▼
┌──────────────────────────┐
│          Cache           │
└──────────────────────────┘
```

### Fluxo básico

O fluxo principal da aplicação funciona da seguinte maneira:

```text
Usuário
   │
   │ informa destino,
   │ duração, orçamento
   │ e interesses
   ▼
Frontend
   │
   │ requisição HTTP
   ▼
Django / REST API
   │
   ├───────────────► Banco de dados
   │
   │ consulta
   ▼
Google Places API
   │
   │ retorna atrações
   ▼
Backend processa
   │
   │ aplica regras
   │ calcula custos
   ▼
Frontend
   │
   ▼
Usuário seleciona
as atrações e monta
seu roteiro
```

### Decisões arquiteturais

#### Django REST Framework

O Django REST Framework será utilizado para estruturar os endpoints da aplicação e estabelecer um contrato padronizado de comunicação entre o frontend e o backend.

#### Separação entre frontend e API externa

A comunicação com a API externa será realizada pelo backend.

O frontend não terá acesso direto à chave da API do Google.

```text
Frontend
    │
    ▼
Backend Django
    │
    ▼
Google Places API
```

Essa abordagem evita a exposição das credenciais e permite que o backend controle o tratamento dos dados recebidos.

#### Resiliência e fallback

Caso a API externa esteja indisponível, exceda seu limite de requisições ou apresente uma falha, o backend deverá tratar o erro e, quando possível, utilizar dados armazenados localmente ou em cache.

#### Cache

Consultas repetidas poderão ser armazenadas temporariamente para reduzir:

* Número de chamadas à API;
* Tempo de resposta;
* Custos da integração;
* Dependência do serviço externo.

#### Variáveis de ambiente

A chave da API externa será armazenada por meio da variável:

```text
GOOGLE_PLACES_API_KEY
```

A chave não deverá ser armazenada diretamente no código-fonte ou versionada no GitHub.

---

### 5.1 Contrato da API

A API própria será disponibilizada inicialmente em:

```text
https://fasttraveller.onrender.com/api/v1
```

> A URL acima deverá ser atualizada caso o endereço definitivo da aplicação seja alterado.

### Endpoints principais

| Método   | Rota                              | Descrição                               |
| :------- | :-------------------------------- | :-------------------------------------- |
| `GET`    | `/api/v1/viagens/`                | Lista as viagens do usuário autenticado |
| `POST`   | `/api/v1/viagens/`                | Cria uma nova viagem                    |
| `GET`    | `/api/v1/viagens/{id}/`           | Consulta uma viagem específica          |
| `PUT`    | `/api/v1/viagens/{id}/`           | Atualiza uma viagem                     |
| `DELETE` | `/api/v1/viagens/{id}/`           | Exclui uma viagem                       |
| `GET`    | `/api/v1/viagens/{id}/atracoes/`  | Consulta as atrações de uma viagem      |
| `GET`    | `/api/v1/viagens/{id}/relatorio/` | Consulta o relatório financeiro         |

### Autenticação

As rotas privadas deverão exigir autenticação.

A implementação poderá utilizar:

* Session Authentication; ou
* Token/JWT.

A escolha definitiva deverá ser feita durante a implementação da API.

### Formato

As requisições e respostas da API utilizarão:

```text
JSON
```

### Códigos HTTP

| Código                      | Significado                              |
| :-------------------------- | :--------------------------------------- |
| `200 OK`                    | Requisição realizada com sucesso         |
| `201 Created`               | Recurso criado com sucesso               |
| `204 No Content`            | Recurso excluído com sucesso             |
| `400 Bad Request`           | Dados inválidos                          |
| `401 Unauthorized`          | Usuário não autenticado                  |
| `403 Forbidden`             | Usuário sem permissão                    |
| `404 Not Found`             | Recurso não encontrado                   |
| `408 Request Timeout`       | Tempo limite excedido                    |
| `429 Too Many Requests`     | Limite de requisições atingido           |
| `500 Internal Server Error` | Erro interno                             |
| `502 Bad Gateway`           | Falha na comunicação com serviço externo |

### Documentação detalhada

O contrato completo da API e o plano de integração externa estão documentados em:

[`docs/api/contrato_e_integracao_api.md`](docs/api/contrato_e_integracao_api.md)

---

## 6. Organização dos diretórios

A estrutura planejada do projeto é:

```text
.
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
│
├── fast_traveller/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── usuarios/
│   ├── viagens/
│   ├── atracoes/
│   └── api/
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── docs/
    ├── visao-geral/
    │   └── visao_geral_e_escopo.md
    │
    ├── requisitos/
    │   └── requisitos_e_regras_de_negocio.md
    │
    ├── banco-de-dados/
    │   ├── modelo_de_dados.md
    │   ├── diagrama_banco.drawio
    │   └── diagrama_banco.png
    │
    ├── api/
    │   └── contrato_e_integracao_api.md
    │
    ├── prototipos/
    │   ├── prototipos_e_identidade_visual.md
    │   └── wireframes_telas.png
    │
    └── planejamento/
        └── backlog_e_planejamento.md
```

### Descrição dos principais diretórios

| Diretório / Arquivo    | Função                                     |
| :--------------------- | :----------------------------------------- |
| `README.md`            | Documentação principal do projeto          |
| `.env.example`         | Modelo das variáveis de ambiente           |
| `.gitignore`           | Arquivos que não devem ser versionados     |
| `requirements.txt`     | Dependências Python do projeto             |
| `manage.py`            | Ponto de entrada administrativo do Django  |
| `fast_traveller/`      | Configurações principais do projeto Django |
| `apps/`                | Aplicações e módulos do sistema            |
| `templates/`           | Templates HTML                             |
| `static/`              | Arquivos CSS, JavaScript e imagens         |
| `docs/visao-geral/`    | Visão geral e escopo                       |
| `docs/requisitos/`     | Requisitos e regras de negócio             |
| `docs/banco-de-dados/` | Modelo e diagramas do banco                |
| `docs/api/`            | Contrato da API e integração externa       |
| `docs/prototipos/`     | Protótipos e identidade visual             |
| `docs/planejamento/`   | Backlog e planejamento das entregas        |

---

## 7. Participantes

| Nome                   | Matrícula | Função no projeto             |
| :--------------------- | :-------- | :---------------------------- |
| [Nome completo]        | [0000000] | Coordenação / Desenvolvimento |
| [Nome do integrante 2] | [0000000] | Backend / Banco de dados      |
| [Nome do integrante 3] | [0000000] | Frontend / Interface          |
| [Nome do integrante 4] | [0000000] | Documentação / Testes         |
| [Nome do integrante 5] | [0000000] | Análise / Planejamento        |

**Professor(a) responsável:** [Nome do(a) professor(a)]

---

## 8. Como executar

> **Observação:** Na Entrega 1, o projeto encontra-se principalmente na etapa de planejamento, documentação e prototipação. As instruções abaixo correspondem ao ambiente previsto para a implementação.

### Pré-requisitos

Antes de executar o projeto, é necessário possuir:

* Git;
* Python 3.11 ou superior;
* pip;
* Ambiente virtual Python.

### 8.1 Clonar o repositório

```bash
git clone https://github.com/[seu-usuario]/fast-traveller.git
cd fast-traveller
```

### 8.2 Criar o ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 8.3 Instalar as dependências

```bash
pip install -r requirements.txt
```

### 8.4 Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

No Linux/macOS:

```bash
cp .env.example .env
```

No Windows:

```powershell
copy .env.example .env
```

Depois, preencha as variáveis necessárias.

### 8.5 Executar as migrações

```bash
python manage.py migrate
```

### 8.6 Executar o servidor

```bash
python manage.py runserver
```

O sistema estará disponível em:

```text
http://127.0.0.1:8000/
```

---

## 9. Configuração

O projeto utiliza variáveis de ambiente para armazenar configurações e informações sensíveis.

### Variáveis previstas

| Variável                | Obrigatória | Descrição                        | Exemplo                       |
| :---------------------- | :---------: | :------------------------------- | :---------------------------- |
| `SECRET_KEY`            |     Sim     | Chave de segurança do Django     | `django-insecure-chave-local` |
| `DEBUG`                 |     Sim     | Ativa/desativa modo de depuração | `True`                        |
| `DATABASE_URL`          |     Não     | URL de conexão do banco          | `sqlite:///db.sqlite3`        |
| `GOOGLE_PLACES_API_KEY` |     Sim     | Chave da API do Google Places    | `sua-chave-aqui`              |

### Exemplo de `.env`

```env
SECRET_KEY=django-insecure-chave-local
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
GOOGLE_PLACES_API_KEY=sua-chave-do-google
```

> **Importante:** O arquivo `.env` não deve ser enviado ao GitHub.

O `.gitignore` deverá conter:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 10. Testes

A aplicação deverá possuir testes para validar os principais componentes do sistema.

### Executar testes

```bash
python manage.py test
```

### Tipos de testes

| Tipo            | Ferramenta                 | Objetivo                                          |
| :-------------- | :------------------------- | :------------------------------------------------ |
| **Unitários**   | `unittest` / `pytest`      | Validar regras de negócio e componentes isolados  |
| **Integração**  | Django REST Framework      | Validar endpoints e comunicação entre componentes |
| **API externa** | Mocks / testes controlados | Validar comportamento diante de respostas da API  |
| **Manuais**     | Checklist                  | Validar fluxos de interface e usabilidade         |

### Casos importantes

Os testes deverão contemplar, entre outros:

* Criação de uma viagem;
* Consulta de uma viagem;
* Atualização de uma viagem;
* Exclusão de uma viagem;
* Validação de orçamento;
* Cálculo do saldo restante;
* Consulta de atrações;
* Usuário não autenticado tentando acessar uma rota privada;
* Viagem inexistente;
* Falha da API externa;
* Timeout da API externa;
* Resposta vazia da API externa.

---

## 11. Uso de inteligência artificial

Este projeto utiliza ferramentas de inteligência artificial como apoio ao processo de desenvolvimento e documentação.

### Situação

**Uso de IA permitido como ferramenta de auxílio.**

### Ferramentas utilizadas

* Google Gemini.

### Finalidades

As ferramentas de IA foram utilizadas para:

* Auxiliar na estruturação da documentação;
* Auxiliar na elaboração do contrato conceitual da API;
* Auxiliar na elaboração de documentação em Markdown;
* Gerar sugestões de layout e estilização;
* Auxiliar na revisão e organização de textos técnicos;

### Responsabilidade da equipe

A utilização de inteligência artificial não substitui a análise e validação dos integrantes do projeto.

A equipe permanece responsável por:

* Definir o problema;
* Definir o escopo;
* Definir as regras de negócio;
* Validar os requisitos;
* Avaliar as sugestões geradas;
* Revisar o código;
* Revisar a documentação;
* Validar os artefatos entregues.

A IA foi utilizada como ferramenta de apoio, e não como substituta da tomada de decisão técnica da equipe.

---

## 12. Contribuição e fluxo de trabalho

O desenvolvimento do projeto será organizado utilizando Git e GitHub.

### Branch principal

```text
main
```

A branch `main` deverá representar uma versão estável do projeto.

### Branches de funcionalidade

Novas funcionalidades deverão utilizar o padrão:

```text
feat/[nome-da-funcionalidade]
```

Exemplos:

```text
feat/autenticacao
feat/criacao-viagem
feat/integracao-google-places
feat/relatorio-financeiro
```

### Branches de documentação

Alterações exclusivamente relacionadas à documentação poderão utilizar:

```text
docs/[nome-do-documento]
```

Exemplos:

```text
docs/readme
docs/contrato-api
docs/modelo-dados
```

### Correções

Para correções:

```text
fix/[nome-da-correcao]
```

Exemplo:

```text
fix/validacao-orcamento
```

---

### Padronização de commits

Os commits deverão possuir mensagens claras e objetivas.

Exemplos:

```text
docs: adiciona contrato de API e integracao externa
```

```text
feat: implementa modelo de dados de viagens
```

```text
feat: adiciona autenticacao de usuarios
```

```text
fix: corrige validacao do orcamento
```

```text
test: adiciona testes para endpoint de viagens
```

```text
refactor: reorganiza servico de integracao externa
```

---

## 13. Histórico de versões

| Versão    | Data       | Descrição                                                                                                                  |
| :-------- | :--------- | :------------------------------------------------------------------------------------------------------------------------- |
| **0.1.0** | 06/10/2026 | Entrega 1 concluída: documentação de visão geral, requisitos, modelo de dados, contrato de API, protótipos e planejamento. |
| **0.0.1** | 06/10/2026 | Estrutura inicial do repositório e organização da documentação.                                                            |

---

## 14. Limitações e próximos passos

### Limitações atuais

Na primeira entrega, o projeto encontra-se principalmente na etapa de:

* Análise;
* Definição do escopo;
* Levantamento de requisitos;
* Modelagem;
* Arquitetura;
* Prototipação;
* Planejamento.

A implementação funcional será desenvolvida nas etapas seguintes.

### Roadmap

#### Sprint 2 — Estrutura e autenticação

* [ ] Inicializar projeto Django.
* [ ] Configurar banco de dados.
* [ ] Criar estrutura das aplicações.
* [ ] Implementar cadastro de usuários.
* [ ] Implementar login.
* [ ] Implementar logout.
* [ ] Criar estrutura inicial da API.
* [ ] Criar modelos de viagem.

#### Sprint 3 — Viagens e atrações

* [ ] Implementar CRUD de viagens.
* [ ] Implementar integração com Google Places API.
* [ ] Implementar busca de atrações.
* [ ] Implementar filtros por categoria.
* [ ] Implementar cache.
* [ ] Implementar tratamento de erros da API externa.
* [ ] Implementar seleção de atrações.

#### Sprint 4 — Roteiro e orçamento

* [ ] Implementar montagem do roteiro.
* [ ] Implementar cálculo de custos.
* [ ] Implementar cálculo do saldo restante.
* [ ] Implementar relatório financeiro.
* [ ] Finalizar integração entre frontend e backend.
* [ ] Executar testes.
* [ ] Corrigir problemas identificados.
* [ ] Preparar versão final para apresentação.

### Evolução futura

Após a implementação do MVP, poderão ser consideradas novas funcionalidades, como:

* Geolocalização do usuário;
* Cálculo de distância entre atrações;
* Otimização da ordem das atrações;
* Integração com mapas;
* Previsão de tempo de deslocamento;
* Recomendações personalizadas;
* Compartilhamento de roteiros;
* Exportação do roteiro;
* Aplicativo mobile.

---

## 15. Licença, referências e contato

### Licença

Este projeto possui finalidade exclusivamente acadêmica e educacional.

Não é permitida a utilização comercial do projeto sem autorização dos respectivos autores.

---

### Referências

1. **Django Web Framework**
   https://www.djangoproject.com/

2. **Django REST Framework**
   https://www.django-rest-framework.org/

3. **Google Places API**
   https://developers.google.com/maps/documentation/places/web-service

4. **Python**
   https://www.python.org/

5. **PostgreSQL**
   https://www.postgresql.org/

6. **Git**
   https://git-scm.com/

7. **GitHub**
   https://github.com/

---

### Documentação interna

A documentação complementar do projeto está organizada em:

```text
docs/
├── visao-geral/
├── requisitos/
├── banco-de-dados/
├── api/
├── prototipos/
└── planejamento/
```

Principais documentos:

* [Visão geral e escopo](docs/visao-geral/visao_geral_e_escopo.md)
* [Requisitos e regras de negócio](docs/requisitos/requisitos_e_regras_de_negocio.md)
* [Modelo de dados](docs/banco-de-dados/modelo_de_dados.md)
* [Contrato e integração da API](docs/api/contrato_e_integracao_api.md)
* [Protótipos e identidade visual](docs/prototipos/prototipos_e_identidade_visual.md)
* [Backlog e planejamento](docs/planejamento/backlog_e_planejamento.md)

---

### Contato

**Repositório do projeto:**

```text
https://github.com/YuriMacedoBolis/Fast-Traveller
```

**Contato do grupo:**

```text
yuribolis2203@gmail.com
viniciusgabrielcoutomachado@gmail.com
```

