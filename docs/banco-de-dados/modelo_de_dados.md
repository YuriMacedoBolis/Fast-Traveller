# Modelo de Banco de Dados - fast Traveller

## 1. Visão Geral
O banco de dados relacional foi modelado para suportar o cadastro de usuários, gestão de viagens, armazenamento de atrações/locais e geração dos roteiros personalizados do **fast Traveller**.

---

## 2. Dicionário de Dados (Tabelas e Atributos)

### Tabela: `usuarios` (Custom User Model / Django Auth)
Armazena as informações dos usuários autenticados no sistema.
* **`id`**: `INT` | Chave Primária (Auto Incremento)
* **`username`**: `VARCHAR(150)` | Único, Obrigatório
* **`email`**: `VARCHAR(254)` | Único, Obrigatório
* **`password`**: `VARCHAR(128)` | Hash da senha do usuário
* **`first_name`**: `VARCHAR(150)` | Nome
* **`last_name`**: `VARCHAR(150)` | Sobrenome
* **`date_joined`**: `DATETIME` | Data de cadastro no sistema

---

### Tabela: `viagens` (Roteiros do Usuário)
Armazena os parâmetros das viagens criadas pelos usuários.
* **`id`**: `INT` | Chave Primária (Auto Incremento)
* **`usuario_id`**: `INT` | Chave Estrangeira -> `usuarios(id)` (ON DELETE CASCADE)
* **`destino`**: `VARCHAR(200)` | Cidade ou local de destino (Ex: "São Paulo, SP")
* **`duracao_dias`**: `INT` | Tempo de permanência do usuário
* **`orcamento_total`**: `DECIMAL(10, 2)` | Valor máximo disponível para gastos (R$)
* **`data_inicio`**: `DATE` | Data de início da viagem
* **`data_criacao`**: `DATETIME` | Registro de quando o roteiro foi criado no sistema

---

### Tabela: `categorias`
Categorias de lazer e atividades escolhidas pelo viajante.
* **`id`**: `INT` | Chave Primária (Auto Incremento)
* **`nome`**: `VARCHAR(100)` | Nome da categoria (Ex: "Cinema", "Museu", "Gastronomia", "Shopping")

---

### Tabela: `atracao_viagem` (Itens do Roteiro / Tabela de Junção)
Armazena as atrações/locais recomendados para uma viagem específica, incluindo dados obtidos via API externa.
* **`id`**: `INT` | Chave Primária (Auto Incremento)
* **`viagem_id`**: `INT` | Chave Estrangeira -> `viagens(id)` (ON DELETE CASCADE)
* **`categoria_id`**: `INT` | Chave Estrangeira -> `categorias(id)`
* **`nome`**: `VARCHAR(255)` | Nome da atração ou local (Ex: "Museu do MASP")
* **`custo_estimado`**: `DECIMAL(10, 2)` | Custo previsto para a atividade
* **`tempo_estimado_horas`**: `DECIMAL(4, 2)` | Duração média da atividade
* **`endereco`**: `VARCHAR(255)` | Endereço ou localização
* **`api_external_id`**: `VARCHAR(255)` | Identificador da atração na API de terceiros (opcional)

---

## 3. Relacionamentos e Cardinalidades

* **`usuarios` $\rightarrow$ `viagens`**: **1 : N**
  * Um usuário pode cadastrar **várias** viagens ($1..N$).
  * Uma viagem pertence obrigatoriamente a **um único** usuário ($1..1$).

* **`viagens` $\rightarrow$ `atracao_viagem`**: **1 : N**
  * Uma viagem pode conter **várias** atrações recomendadas no seu roteiro ($1..N$).
  * Uma atração listada pertence a **uma única** viagem ($1..1$).

* **`categorias` $\rightarrow$ `atracao_viagem`**: **1 : N**
  * Uma categoria pode estar associada a **várias** atrações ($1..N$).
  * Uma atração pertence a **uma** categoria ($1..1$).