# Contrato de API e Plano de Integração Externa - fast Traveller

## 1. Visão Geral

O **fast Traveller** utilizará uma API REST própria, desenvolvida com **Django REST Framework (DRF)**, para permitir que o frontend da aplicação e serviços autorizados consultem e gerenciem os dados relacionados às viagens dos usuários.

A aplicação também realizará integração com uma **API externa de localização e pontos de interesse**, permitindo buscar atrações reais de acordo com o destino e as preferências informadas pelo usuário.

### Informações gerais da API própria

| Item              | Definição                                   |
| ----------------- | ------------------------------------------- |
| URL Base          | `https://fasttraveller.onrender.com/api/v1` |
| Arquitetura       | REST                                        |
| Formato dos dados | JSON                                        |
| Framework         | Django REST Framework                       |
| Autenticação      | Session Authentication ou Token/JWT         |
| Comunicação       | HTTP/HTTPS                                  |

As rotas relacionadas aos dados pessoais e às viagens dos usuários serão protegidas por autenticação.

---

# Parte 1 — Contrato Inicial da API REST Própria

## 2. Endpoints da API

A API própria será responsável principalmente pelo gerenciamento das viagens, atrações e informações relacionadas ao planejamento financeiro.

Os principais recursos serão:

* Viagens;
* Atrações;
* Roteiros;
* Relatórios de gastos.

---

## 2.1 Listar e Criar Viagens

### Endpoint

```http
GET /api/v1/viagens/
POST /api/v1/viagens/
```

### Autenticação

**Requerida.**

### GET `/viagens/`

Retorna a lista de viagens cadastradas pelo usuário autenticado.

#### Resposta de sucesso

**HTTP 200 OK**

```json
[
  {
    "id": 1,
    "destino": "São Paulo, SP",
    "duracao_dias": 3,
    "orcamento_total": 1500.00,
    "data_inicio": "2026-11-10",
    "data_criacao": "2026-10-06T15:30:00Z"
  }
]
```

### POST `/viagens/`

Cria uma nova viagem com os parâmetros informados pelo usuário.

#### Corpo da requisição

```json
{
  "destino": "Rio de Janeiro, RJ",
  "duracao_dias": 2,
  "orcamento_total": 800.00,
  "data_inicio": "2026-12-01"
}
```

#### Resposta de sucesso

**HTTP 201 Created**

```json
{
  "id": 2,
  "destino": "Rio de Janeiro, RJ",
  "duracao_dias": 2,
  "orcamento_total": 800.00,
  "data_inicio": "2026-12-01",
  "data_criacao": "2026-10-06T19:00:00Z"
}
```

---

## 2.2 Obter, Atualizar ou Excluir uma Viagem

### Endpoint

```http
GET /api/v1/viagens/{id}/
PUT /api/v1/viagens/{id}/
DELETE /api/v1/viagens/{id}/
```

### Autenticação

**Requerida.**

O endpoint permite consultar, atualizar ou excluir uma viagem específica por meio do seu identificador.

### GET

Retorna os dados da viagem solicitada.

#### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "id": 1,
  "destino": "São Paulo, SP",
  "duracao_dias": 3,
  "orcamento_total": 1500.00,
  "data_inicio": "2026-11-10",
  "data_criacao": "2026-10-06T15:30:00Z"
}
```

### PUT

Atualiza os dados de uma viagem existente.

#### Exemplo de requisição

```json
{
  "destino": "São Paulo, SP",
  "duracao_dias": 4,
  "orcamento_total": 1800.00,
  "data_inicio": "2026-11-10"
}
```

#### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "id": 1,
  "destino": "São Paulo, SP",
  "duracao_dias": 4,
  "orcamento_total": 1800.00,
  "data_inicio": "2026-11-10",
  "data_criacao": "2026-10-06T15:30:00Z"
}
```

### DELETE

Exclui uma viagem existente.

#### Resposta de sucesso

**HTTP 204 No Content**

### Possíveis erros

| Código             | Situação                     |
| ------------------ | ---------------------------- |
| `401 Unauthorized` | Usuário não autenticado      |
| `403 Forbidden`    | Usuário não possui permissão |
| `404 Not Found`    | Viagem não encontrada        |
| `400 Bad Request`  | Dados enviados são inválidos |

---

## 2.3 Consultar Roteiro e Atrações de uma Viagem

### Endpoint

```http
GET /api/v1/viagens/{id}/atracoes/
```

### Autenticação

**Requerida.**

O endpoint retorna as atrações associadas a uma viagem específica.

Essas atrações podem ser provenientes de dados cadastrados localmente ou de informações obtidas por meio da API externa de pontos de interesse.

### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "viagem_id": 1,
  "destino": "São Paulo, SP",
  "atracoes": [
    {
      "id": 10,
      "nome": "MASP - Museu de Arte de São Paulo",
      "categoria": "museu",
      "custo_estimado": 50.00,
      "tempo_estimado_horas": 2.5,
      "endereco": "Av. Paulista, 1578"
    },
    {
      "id": 11,
      "nome": "Cine Sesc",
      "categoria": "cinema",
      "custo_estimado": 24.00,
      "tempo_estimado_horas": 2.0,
      "endereco": "R. Augusta, 2075"
    }
  ]
}
```

### Possíveis erros

| Código             | Situação                     |
| ------------------ | ---------------------------- |
| `401 Unauthorized` | Usuário não autenticado      |
| `403 Forbidden`    | Usuário não possui permissão |
| `404 Not Found`    | Viagem não encontrada        |

---

## 2.4 Consultar Relatório de Gastos e Indicadores

### Endpoint

```http
GET /api/v1/viagens/{id}/relatorio/
```

### Autenticação

**Requerida.**

O endpoint disponibiliza informações consolidadas sobre o orçamento da viagem e os custos estimados das atrações selecionadas.

### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "viagem_id": 1,
  "destino": "São Paulo, SP",
  "orcamento_total": 1500.00,
  "custo_total_estimado": 74.00,
  "saldo_restante": 1426.00,
  "total_atracoes": 2,
  "gastos_por_categoria": {
    "museu": 50.00,
    "cinema": 24.00
  }
}
```

### Indicadores disponibilizados

O relatório poderá apresentar:

* Orçamento total da viagem;
* Custo total estimado das atrações;
* Saldo restante;
* Quantidade de atrações selecionadas;
* Distribuição dos gastos por categoria.

---

# Parte 2 — Plano de Integração com API Externa

## 3. API Externa Selecionada

### Google Places API

A API externa inicialmente selecionada para o projeto é a **Google Places API**, podendo ser utilizada a **OpenStreetMap Overpass API** como alternativa de menor custo.

A integração terá como objetivo buscar pontos de interesse reais existentes no destino escolhido pelo usuário.

Entre os exemplos de locais que poderão ser encontrados estão:

* Museus;
* Cinemas;
* Restaurantes;
* Shoppings;
* Parques;
* Pontos turísticos;
* Outros estabelecimentos e locais de interesse.

---

## 4. Finalidade da Integração

O usuário informará dados relacionados à viagem, como:

* Destino;
* Quantidade de dias ou horas disponíveis;
* Orçamento;
* Categorias de interesse.

Com essas informações, o backend poderá consultar a API externa para encontrar locais compatíveis com o destino e os interesses selecionados.

### Exemplo

O usuário informa:

```text
Destino: São Paulo
Duração: 3 dias
Orçamento: R$ 1.500
Interesses: Museus e Cinema
```

O backend poderá realizar consultas semelhantes a:

```text
museus em São Paulo
cinemas em São Paulo
```

A API externa retornará informações sobre os estabelecimentos encontrados.

O sistema poderá então processar esses dados e apresentá-los ao usuário como opções para composição do seu roteiro.

---

# 5. Endpoint Externo Consumido

Para a integração inicial com o Google Places API será utilizado o endpoint de busca por texto.

```http
GET https://maps.googleapis.com/maps/api/place/textsearch/json
```

### Parâmetros enviados

| Parâmetro | Descrição                             | Exemplo                 |
| --------- | ------------------------------------- | ----------------------- |
| `query`   | Texto utilizado para realizar a busca | `museus em São Paulo`   |
| `key`     | Chave de autenticação da API          | `GOOGLE_PLACES_API_KEY` |

### Exemplo de requisição conceitual

```http
GET https://maps.googleapis.com/maps/api/place/textsearch/json?query=museus+em+São+Paulo&key=GOOGLE_PLACES_API_KEY
```

A requisição será realizada pelo **backend**, e não diretamente pelo frontend.

---

# 6. Dados Consumidos da API Externa

O sistema utilizará principalmente informações relacionadas à identificação e localização dos pontos de interesse.

Entre os dados relevantes estão:

| Campo               | Utilização no fast Traveller               |
| ------------------- | ------------------------------------------ |
| `name`              | Nome do estabelecimento ou ponto turístico |
| `formatted_address` | Endereço do local                          |
| `price_level`       | Estimativa da faixa de preço               |
| `types`             | Categorias/tipos do local                  |

Esses dados serão processados pelo backend antes de serem disponibilizados ao frontend.

---

# 7. Fluxo de Integração

O fluxo básico da integração será:

```text
┌─────────────────────┐
│       Usuário       │
└──────────┬──────────┘
           │
           │ Informa destino,
           │ orçamento e interesses
           ▼
┌─────────────────────┐
│      Frontend       │
└──────────┬──────────┘
           │
           │ Requisição
           ▼
┌─────────────────────┐
│  API própria DRF    │
│      Backend        │
└──────────┬──────────┘
           │
           │ Consulta pontos
           │ de interesse
           ▼
┌─────────────────────┐
│   Google Places     │
│        API          │
└──────────┬──────────┘
           │
           │ Resultados
           ▼
┌─────────────────────┐
│  Backend processa   │
│       dados         │
└──────────┬──────────┘
           │
           │ Dados filtrados
           ▼
┌─────────────────────┐
│      Frontend       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Sugestões de locais │
│      e roteiro      │
└─────────────────────┘
```

Dessa forma, o frontend não terá contato direto com a chave da API externa.

---

# 8. Tratamento de Erros e Indisponibilidade

A integração deverá considerar possíveis falhas na comunicação com a API externa.

## 8.1 Timeout

As chamadas realizadas pelo backend terão um tempo limite de aproximadamente **5 segundos**.

Caso a API não responda dentro desse período, a aplicação deverá interromper a requisição para evitar que o usuário fique aguardando indefinidamente.

### Exemplo conceitual

```python
try:
    response = requests.get(
        url,
        params=params,
        timeout=5
    )
except requests.Timeout:
    # Utilizar dados locais ou retornar resposta alternativa
    ...
```

---

## 8.2 Falha na API Externa

Caso a API externa esteja indisponível ou apresente algum erro, o sistema não deverá interromper completamente a navegação do usuário.

O backend poderá utilizar dados previamente armazenados no banco de dados local.

O comportamento esperado será:

```text
API externa disponível
        │
        ▼
Consulta realizada
        │
        ▼
Resultados processados
        │
        ▼
Dados apresentados ao usuário
```

Em caso de indisponibilidade:

```text
API externa indisponível
        │
        ▼
Erro capturado pelo backend
        │
        ▼
Consulta aos dados locais
        │
        ▼
Dados disponíveis apresentados
```

Isso permite que a aplicação continue funcionando mesmo quando o serviço externo apresentar instabilidade.

---

# 9. Cache e Controle de Requisições

Para evitar requisições desnecessárias à API externa, será utilizado um mecanismo de **cache interno**.

Por exemplo, uma consulta como:

```text
museus em São Paulo
```

poderá ter seu resultado armazenado temporariamente.

Caso outro usuário faça uma consulta equivalente dentro do período de validade do cache, o sistema poderá reutilizar os dados armazenados em vez de realizar uma nova requisição à API externa.

### Benefícios

* Redução da quantidade de chamadas à API;
* Redução de custos;
* Menor tempo de resposta;
* Menor dependência da API externa;
* Maior estabilidade da aplicação.

---

# 10. Segurança das Credenciais

A chave da API externa será tratada como um **segredo da aplicação**.

A chave não deverá ser:

* Inserida diretamente no código-fonte;
* Enviada ao frontend;
* Publicada no GitHub;
* Inserida diretamente em arquivos versionados.

Será utilizada uma variável de ambiente:

```text
GOOGLE_PLACES_API_KEY
```

Em ambiente de desenvolvimento, a variável poderá ser armazenada em um arquivo `.env`, desde que esse arquivo esteja incluído no `.gitignore`.

### Exemplo

```env
GOOGLE_PLACES_API_KEY=sua_chave_aqui
```

No ambiente de produção, a variável deverá ser configurada diretamente no serviço de hospedagem.

---

# 11. Arquitetura da Integração

A arquitetura proposta pode ser representada da seguinte maneira:

```text
                     ┌─────────────────┐
                     │     Frontend    │
                     └────────┬────────┘
                              │
                              │ HTTPS / JSON
                              ▼
                     ┌─────────────────┐
                     │   Django REST   │
                     │    Framework    │
                     └────────┬────────┘
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
        ┌────────────┐ ┌─────────────┐ ┌─────────────┐
        │  Banco de  │ │    Cache    │ │ Google      │
        │   Dados    │ │             │ │ Places API  │
        └────────────┘ └─────────────┘ └─────────────┘
```

O backend será responsável por centralizar a comunicação entre o frontend, o banco de dados, o mecanismo de cache e a API externa.

---

# 12. Responsabilidades de Cada Camada

## Frontend

Responsável por:

* Coletar informações do usuário;
* Enviar requisições para a API própria;
* Exibir viagens;
* Exibir atrações;
* Apresentar sugestões de roteiro;
* Exibir informações financeiras.

O frontend não deverá armazenar ou expor a chave da API externa.

## Backend — Django REST Framework

Responsável por:

* Autenticação;
* Autorização;
* Gerenciamento das viagens;
* Gerenciamento das atrações;
* Comunicação com a API externa;
* Validação dos dados;
* Tratamento de erros;
* Aplicação de regras de negócio;
* Cache das consultas;
* Geração dos relatórios.

## Banco de Dados

Responsável por armazenar:

* Usuários;
* Viagens;
* Atrações selecionadas;
* Dados necessários para o roteiro;
* Informações relacionadas aos gastos.

## API Externa

Responsável por fornecer informações sobre pontos de interesse reais existentes nos destinos pesquisados.

---

# 13. Códigos HTTP Utilizados

A API seguirá códigos HTTP convencionais para indicar o resultado das operações.

| Código                      | Significado                                | Utilização          |
| --------------------------- | ------------------------------------------ | ------------------- |
| `200 OK`                    | Requisição realizada com sucesso           | GET e PUT           |
| `201 Created`               | Recurso criado                             | POST                |
| `204 No Content`            | Operação realizada sem conteúdo de retorno | DELETE              |
| `400 Bad Request`           | Dados enviados são inválidos               | Validação           |
| `401 Unauthorized`          | Usuário não autenticado                    | Rotas privadas      |
| `403 Forbidden`             | Usuário não possui permissão               | Acesso indevido     |
| `404 Not Found`             | Recurso não encontrado                     | Viagem inexistente  |
| `408 Request Timeout`       | Tempo limite excedido                      | Comunicação externa |
| `429 Too Many Requests`     | Limite de requisições atingido             | API externa         |
| `500 Internal Server Error` | Erro interno do servidor                   | Falha inesperada    |
| `502 Bad Gateway`           | Falha na comunicação com serviço externo   | API externa         |

---

# 14. Considerações sobre a API Externa

A utilização de uma API externa permite que o **fast Traveller** trabalhe com informações reais sobre os destinos sem precisar cadastrar manualmente todos os pontos turísticos e estabelecimentos disponíveis.

Entretanto, a aplicação não deverá depender exclusivamente da disponibilidade do serviço externo.

Por isso, a arquitetura prevê:

1. Comunicação exclusivamente pelo backend;
2. Proteção da chave de API;
3. Timeout das requisições;
4. Tratamento de exceções;
5. Cache das consultas;
6. Utilização de dados locais como fallback.

---

# 15. Referência da API

Documentação oficial da Google Places API:

```text
https://developers.google.com/maps/documentation/places/web-service/overview
```

A documentação deverá ser consultada durante a implementação para verificar os parâmetros, limites, custos, autenticação e versões disponíveis da API utilizada.

---

# 16. Resumo do Contrato

### API própria

```text
GET    /api/v1/viagens/
POST   /api/v1/viagens/

GET    /api/v1/viagens/{id}/
PUT    /api/v1/viagens/{id}/
DELETE /api/v1/viagens/{id}/

GET    /api/v1/viagens/{id}/atracoes/

GET    /api/v1/viagens/{id}/relatorio/
```

### API externa

```text
GET https://maps.googleapis.com/maps/api/place/textsearch/json
```

### Principais responsabilidades

```text
Frontend
   ↓
API REST própria
   ↓
Django REST Framework
   ↓
Banco de Dados + Cache
   ↓
API de pontos de interesse
```

A API própria será responsável pelas regras de negócio e pelos dados do usuário, enquanto a API externa será utilizada como fonte complementar de informações sobre locais e atrações dos destinos.
