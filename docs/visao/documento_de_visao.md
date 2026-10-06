# Documento de Visão - fast Traveller

## 1. Contexto e Problema
* **Contexto:** Turistas e viajantes frequentemente enfrentam dificuldades para planejar itinerários diários que respeitem seu orçamento, tempo disponível e preferências pessoais de entretenimento.
* **Problema:** A falta de uma ferramenta centralizada que recomende atrações e atividades filtradas por custo, localização e disponibilidade de tempo.

## 2. Justificativa e Objetivos
* **Justificativa:** O *fast Traveller* simplifica a tomada de decisão em viagens, sugerindo roteiros otimizados sem que o usuário precise pesquisar em múltiplas plataformas.
* **Objetivo Geral:** Desenvolver uma aplicação web em Python e Django que ajude viajantes a planejar suas atividades com base em tempo, orçamento e categorias de interesse.

## 3. Público-Alvo e Stakeholders
* **Público-Alvo:** Turistas, viajantes solo, famílias ou grupos em busca de roteiros personalizados rápidos.
* **Stakeholders:** Usuários finais (turistas/viajantes), equipe de desenvolvimento e corpo docente/avaliadores da disciplina.

## 4. Escopo do Projeto
* **Itens no Escopo:**
  * Cadastro, login e autenticação de usuários.
  * Formulário de entrada com: localização atual/destino, duração da estadia, orçamento disponível e preferências de lazer (cinema, museu, gastronomia, shopping, etc.).
  * Geração e exibição de sugestões de roteiro adaptadas ao perfil informado.
  * Histórico de viagens e roteiros salvos pelo usuário (operações CRUD).
  * Consumo de API externa para obtenção de pontos de interesse/locais reais.
  * API REST própria para consulta de dados cadastrados.
  * Relatório com dados consolidados e opção de exportação/impressão.
* **Itens Fora do Escopo:**
  * Reserva ou pagamento direto de passagens, hotéis ou ingressos dentro do sistema.
  * Sistema de chat em tempo real entre viajantes.

## 5. Restrições e Premissas
* **Restrições:** 
  * Backend obrigatoriamente desenvolvido em Python utilizando Django.
  * Banco de dados relacional.
  * Publicação com HTTPS e variável `DEBUG=False` em produção.
* **Premissas:** 
  * Disponibilidade das APIs externas de pontos de interesse durante as requisições.

## 6. Riscos Iniciais e Critérios de Sucesso
* **Riscos:** Indisponibilidade ou limites de cota da API externa utilizada; complexidade na ordenação e cálculo do orçamento do roteiro.
* **Critérios de Sucesso:** Aplicação totalmente funcional, publicada, segura e em conformidade com todos os requisitos funcionais e não funcionais da disciplina.