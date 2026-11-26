# Relatório de segurança - fast Traveller

Análise de segurança da aplicação com SAST (análise estática) e DAST (análise dinâmica), feita antes e depois das correções.

Data: 25/11/2026 · Branch: `feat/seguranca`

## Ferramentas

| Tipo | Ferramenta | Versão | O que verifica |
| :--- | :--------- | :----- | :------------- |
| SAST | bandit | 1.9.4 | Padrões inseguros no código Python |
| SAST | pip-audit | 2.10.1 | Vulnerabilidades conhecidas (CVE/PYSEC) nas dependências |
| SAST | `manage.py check --deploy` | Django 5.2.19 | Configurações de produção do Django |
| DAST | OWASP ZAP | 2.17.0 | Varredura passiva e ativa da aplicação rodando |

## Resumo

| Verificação | Antes | Depois |
| :---------- | :---- | :----- |
| bandit (código da aplicação) | 0 problemas | 0 problemas |
| pip-audit `requirements.txt` | 51 vulnerabilidades (Django 5.2.9) | 0 |
| pip-audit `requirements-dev.txt` | 2 vulnerabilidades (pytest 8.4.2) | 0 |
| `check --deploy` (DEBUG=False) | 0 avisos | 0 avisos |
| ZAP - risco Médio | 3 | 2 (aceitos, ver abaixo) |
| ZAP - risco Baixo | 3 | 1 (aceito, ver abaixo) |
| ZAP - Informativo | 5 | 5 |

## SAST

### bandit

Comando:

```bash
bandit -r contas core viagens -x "*/tests/*,*/migrations/*"
```

Nenhum problema encontrado no código da aplicação, nem antes nem depois das alterações. Os testes ficaram fora da análise porque usam senhas fixas de propósito (usuários de teste), o que geraria falsos positivos.

Relatórios: [`bandit-antes.txt`](bandit-antes.txt), [`bandit-depois.txt`](bandit-depois.txt).

### pip-audit

Comando:

```bash
pip-audit -r requirements.txt
pip-audit -r requirements-dev.txt
```

| Pacote | Versão antes | Vulnerabilidades | Correção |
| :----- | :----------- | :--------------- | :------- |
| Django | 5.2.9 | 51 (ex.: PYSEC-2026-42, enumeração de usuários por timing) | Atualizado para 5.2.19, último patch da mesma versão LTS |
| pytest | 8.4.2 | 1 (PYSEC-2026-1845, diretório temporário previsível) | Atualizado para 9.0.3 |

Depois da atualização os 43 testes continuaram passando e o pip-audit não encontrou mais nenhuma vulnerabilidade.

Relatórios: [`pip-audit-antes.txt`](pip-audit-antes.txt), [`pip-audit-depois.txt`](pip-audit-depois.txt), [`pip-audit-dev-antes.txt`](pip-audit-dev-antes.txt), [`pip-audit-dev-depois.txt`](pip-audit-dev-depois.txt).

### check --deploy

Executado com `DJANGO_DEBUG=False` para simular produção. Sem avisos: HSTS, cookies `Secure`, redirecionamento para HTTPS e `SECRET_KEY` já estavam configurados no `settings.py` para quando `DEBUG` é falso.

Relatório: [`check-deploy.txt`](check-deploy.txt).

## DAST - OWASP ZAP

### Como foi executado

- Alvo: servidor local (`python manage.py runserver`) com banco SQLite de teste. Produção (Render) não foi escaneada.
- Plano: [`zap-plano.yaml`](zap-plano.yaml), rodado com `zap.bat -cmd -autorun zap-plano.yaml`.
- Autenticação: um usuário de teste logado, com o cookie de sessão injetado pelo job `replacer`. Assim o ZAP também testou as páginas privadas (lista, roteiro, relatório, CSV e API).
- Excluídos da varredura ativa: `/logout/` (encerraria a sessão), `/viagens/<id>/excluir/` (apagaria os dados de teste), `/admin/` e `/static/`.
- Etapas: spider, requisições às rotas principais, varredura passiva e varredura ativa.

Relatórios: [`zap-antes.md`](zap-antes.md), [`zap-depois.md`](zap-depois.md). As versões HTML e JSON ficam só na máquina local (estão no `.gitignore`).

### Alertas e tratamento

| Alerta | Risco | Antes | Depois | Tratamento |
| :----- | :---- | :---: | :----: | :--------- |
| Content Security Policy (CSP) Header Not Set | Médio | 5 | 0 | Corrigido |
| Sub Resource Integrity Attribute Missing | Médio | 5 | 5 | Parcial: CDN do Swagger removida; Google Fonts aceito |
| HTTP Only Site | Médio | 1 | 1 | Aceito: só no ambiente local |
| Cookie No HttpOnly Flag | Baixo | 5 | 0 | Corrigido |
| Cross-Domain JavaScript Source File Inclusion | Baixo | 2 | 0 | Corrigido |
| Server Leaks Version Information | Baixo | 5 | 5 | Aceito: servidor de desenvolvimento |
| Informativos (5 tipos) | Info | 23 | 22 | Sem ação |

### Correções aplicadas

**1. Content-Security-Policy e Permissions-Policy**

Criado o middleware `core/middleware.py`, que adiciona em todas as respostas:

```text
Content-Security-Policy: default-src 'self'; script-src 'self';
  style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self';
  form-action 'self'; frame-ancestors 'none'
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

A política não usa `unsafe-inline`. Para isso, os dois estilos inline do projeto foram trocados: o formulário de sair ganhou a classe `.form-sair` e a largura das barras do relatório passou a ser aplicada pelo `relatorio.js` a partir do atributo `data-porcentagem`. Os dados que as páginas passam ao JavaScript usam `json_script`, que não é executado e por isso não é bloqueado.

**2. Documentação da API sem scripts externos**

O `/api/docs/` carregava o Swagger UI de uma CDN (`cdn.jsdelivr.net`) e tinha um script inline. Agora usa o `drf-spectacular-sidecar`, que serve os arquivos do próprio servidor, e a `SpectacularSwaggerSplitView`, que coloca o script de inicialização num arquivo separado. Isso resolveu o alerta de JavaScript de outro domínio, o SRI da CDN e deixou o Swagger funcionando com a CSP. A rota `/api/redoc/` foi removida porque duplicava o Swagger e depende de estilos inline.

**3. Cookie CSRF com HttpOnly**

`CSRF_COOKIE_HTTPONLY = True` no `settings.py`. O JavaScript do roteiro lê o token do campo escondido gerado por `{% csrf_token %}`, e o Swagger recebe o token pelo template, então nenhum dos dois precisa ler o cookie.

### Riscos aceitos

| Alerta | Motivo |
| :----- | :----- |
| SRI no Google Fonts | O CSS do Google Fonts muda conforme o navegador que pede, então não existe um hash fixo para colocar no `integrity`. O risco é limitado pela CSP, que só permite estilos de `fonts.googleapis.com` e fontes de `fonts.gstatic.com`. Alternativa futura: hospedar a fonte Inter no próprio projeto. |
| HTTP Only Site | A varredura foi feita no servidor local, que não tem HTTPS. Em produção (`DEBUG=False`) o `settings.py` ativa `SECURE_SSL_REDIRECT`, HSTS de 1 ano e cookies `Secure`, e o Render serve só HTTPS. |
| Server Leaks Version Information | O header `Server: WSGIServer/0.2 CPython/3.13` vem do `runserver`, que é só para desenvolvimento. Em produção a aplicação roda com gunicorn. |

### Alertas informativos

Não indicam vulnerabilidade: "Authentication Request Identified" e "Session Management Response Identified" só registram que existem login e cookie de sessão; "Modern Web Application" indica que o Swagger usa JavaScript; "User Agent Fuzzer" mostra que as páginas respondem igual para qualquer navegador; "User Controllable HTML Element Attribute" aponta que o parâmetro `next` do login aparece num atributo HTML, mas o Django escapa o valor e só aceita redirecionamento para o próprio site.

## Outros controles já existentes

- Senhas com hash do Django e validadores de senha.
- Todas as páginas e endpoints de viagem exigem login e filtram pelo dono (outro usuário recebe 404), com testes cobrindo isso.
- Proteção CSRF em todos os formulários e chamadas `fetch` que alteram dados.
- Limite de requisições na API (`120/hour` por usuário e `30/hour` nas sugestões).
- Chave da Geoapify só no backend, em variável de ambiente.
- Exportação CSV neutraliza células que começam com `=`, `+`, `-`, `@`, tab ou quebra de linha, evitando injeção de fórmula no Excel.
- Nomes vindos da API externa são inseridos na página com `textContent`, nunca como HTML.

## Como reproduzir

```bash
pip install -r requirements-dev.txt
bandit -r contas core viagens -x "*/tests/*,*/migrations/*"
pip-audit -r requirements.txt
```

Para o ZAP: rodar o servidor local, criar um usuário de teste e uma viagem, definir as variáveis `ZAP_SESSAO` (cookie `sessionid`), `ZAP_VIAGEM` (id da viagem), `ZAP_SAIDA` (pasta de saída) e `ZAP_NOME` (nome do relatório) e executar `zap.bat -cmd -autorun security/zap-plano.yaml`.
