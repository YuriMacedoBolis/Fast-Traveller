# Protótipos e Identidade Visual - fast Traveller

## 1. Guia de Estilo e Identidade Visual

### Concept & Proposta
O **fast Traveller** visa oferecer uma experiência de navegação ágil, intuitiva e moderna para o planeamento de viagens sem complicações. A paleta de cores reflete a sensação de descoberta, dinamismo e organização financeira.

### Paleta de Cores Principais
* **Cor Primária (Azul Viagem):** `#1E3A8A` — Transmite confiança, organização e serenidade.
* **Cor Secundária (Laranja Aventura):** `#F97316` — Utilizada em botões de ação (CTAs), destaques e elementos interativos.
* **Cores de Apoio:**
  * **Fundo Claro:** `#F8FAFC`
  * **Texto Principal:** `#0F172A`
  * **Sucesso / Saldo Positivo:** `#16A34A`
  * **Alerta / Limite de Orçamento:** `#DC2626`

### Tipografia
* **Fonte Principal (Interface):** `Inter` ou `Roboto` (Sans-serif moderna, de alta legibilidade).
* **Hierarquia:**
  * **Título Principal (H1):** Bold, 32px
  * **Subtítulos (H2 / H3):** Semi-bold, 24px / 18px
  * **Corpo do Texto:** Regular, 16px
  * **Legendas e Acessórios:** Regular, 14px

---

## 2. Estrutura das Telas e Fluxo do Utilizador

O sistema é composto por 5 telas principais que cobrem todo o fluxo da aplicação:

1. **Tela de Login / Cadastro (`/login`, `/cadastro`):**
   * Formulário simples de autenticação com validação de campos obrigatórios e criação de conta.
2. **Dashboard / Minhas Viagens (`/viagens`):**
   * Listagem em cards das viagens criadas pelo utilizador, com opção de criar uma nova viagem ou aceder a um roteiro existente.
3. **Formulário de Nova Viagem (`/viagens/nova`):**
   * Entrada de dados: Destino, Duração em dias, Orçamento total em R$ e seleção de categorias de interesse (ex: museus, cinema, gastronomia).
4. **Detalhes do Roteiro e Atrações (`/viagens/{id}`):**
   * Exibição das atrações sugeridas via API externa, organizadas por dia/categoria com opção de selecionar/desmarcar atrações.
5. **Relatório Financeiro e Gastos (`/viagens/{id}/relatorio`):**
   * Dashboard com gráficos/tabelas exibindo a distribuição dos custos por categoria, orçamento total e saldo restante.

---

