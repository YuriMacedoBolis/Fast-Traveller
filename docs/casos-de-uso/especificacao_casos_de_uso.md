# Especificação de Casos de Uso - fast Traveller

## Atores
* **Viajante / Turista:** Usuário do sistema que cadastra preferências, planeja e salva roteiros de viagem.
* **Sistema Explicito / API Externa:** Serviço terceiro de geolocalização e locais/atrações (ex: Google Places API / TripAdvisor).

---

## UC01 - Cadastrar e Autenticar Usuário
* **Ator Principal:** Viajante
* **Objetivo:** Permitir que o usuário crie uma conta no sistema e faça login de forma segura.
* **Pré-condições:** O usuário deve ter um e-mail válido.
* **Pós-condições:** O usuário é autenticado e obtém acesso às áreas restritas do sistema.
* **Fluxo Principal:**
  1. O usuário acessa a tela de cadastro/login.
  2. O usuário informa e-mail, nome e senha.
  3. O sistema valida os dados recebidos.
  4. O sistema cria o registro de usuário e redireciona para a tela inicial.
* **Fluxo Alternativo (Login):**
  1. O usuário informa e-mail e senha cadastrados.
  2. O sistema autentica o usuário e inicia a sessão.
* **Exceções:**
  * Dados inválidos ou e-mail já cadastrado: o sistema exibe mensagem de erro e solicita novas informações.

---

## UC02 - Criar Roteiro de Viagem
* **Ator Principal:** Viajante
* **Objetivo:** Cadastrar uma nova viagem definindo parâmetros de localização, tempo e orçamento.
* **Pré-condições:** Usuário deve estar autenticado.
* **Pós-condições:** O roteiro é gerado e salvo no histórico do usuário.
* **Fluxo Principal:**
  1. O usuário seleciona a opção "Novo Roteiro".
  2. O usuário informa a localização/destino, duração da estadia (horas/dias), orçamento disponível (R$) e categorias de interesse (ex: cinema, museu, gastronomia, shopping).
  3. O sistema envia a requisição à API Externa para buscar atrações compatíveis na região.
  4. O sistema processa as atrações, calcula os custos estimados e tempo total, exibindo o roteiro sugerido.
  5. O usuário confirma e salva o roteiro.
* **Exceções:**
  * Falha na conexão ou indisponibilidade da API Externa: o sistema exibe mensagem amigável de erro e permite tentar novamente.
  * Nenhuma atração encontrada para o orçamento/tempo informado: o sistema sugere ajustar os filtros.

---

## UC03 - Consultar e Gerenciar Roteiros Salvos (CRUD)
* **Ator Principal:** Viajante
* **Objetivo:** Visualizar, alterar ou excluir roteiros previamente salvos.
* **Pré-condições:** Usuário deve ter pelo menos um roteiro cadastrado.
* **Pós-condições:** Roteiro atualizado ou removido do banco de dados.
* **Fluxo Principal:**
  1. O usuário acessa "Meus Roteiros".
  2. O sistema lista os roteiros cadastrados com filtros por data ou destino.
  3. O usuário pode selecionar um roteiro para visualizar os detalhes, editar itens ou excluí-lo.
* **Exceções:**
  * Roteiro não encontrado: o sistema informa que o registro não existe.

---

## UC04 - Gerar Relatório de Gastos e Atividades
* **Ator Principal:** Viajante
* **Objetivo:** Exibir dados consolidados da viagem (gastos por categoria, total estimado vs. orçamento) com opção de exportação/impressão.
* **Pré-condições:** Roteiro selecionado pelo usuário.
* **Pós-condições:** Relatório visualizado e/ou exportado/impresso.
* **Fluxo Principal:**
  1. O usuário solicita o relatório de um roteiro específico.
  2. O sistema consolida os indicadores (ex: total gasto em alimentação, atrações e tempo total).
  3. O sistema apresenta os dados em tela e disponibiliza os botões "Imprimir" ou "Exportar".