const roteiro = document.getElementById("roteiro");
const orcamento = Number(roteiro.dataset.orcamento);
const urlViagem = `/api/v1/viagens/${roteiro.dataset.viagem}/`;
const csrfToken = roteiro.querySelector("[name=csrfmiddlewaretoken]").value;
const nomesCategorias = JSON.parse(document.getElementById("dados-categorias").textContent);
const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

const formBusca = document.getElementById("form-busca");
const botaoBusca = document.getElementById("botao-busca");
const avisoBusca = document.getElementById("aviso-busca");

let selecionadas = JSON.parse(document.getElementById("dados-atracoes").textContent);
let sugestoes = [];

async function chamarApi(caminho, opcoes = {}) {
  const resposta = await fetch(urlViagem + caminho, {
    ...opcoes,
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  if (!resposta.ok) {
    const dados = await resposta.json().catch(() => ({}));
    throw new Error(dados.detail || "Não foi possível concluir a ação. Tente de novo.");
  }

  if (resposta.status === 204) {
    return null;
  }
  return resposta.json();
}

function mostrarAviso(texto) {
  avisoBusca.textContent = texto;
  avisoBusca.hidden = !texto;
}

function totalSelecionado() {
  return selecionadas.reduce((soma, atracao) => soma + Number(atracao.custo_estimado), 0);
}

function atualizarResumo() {
  const total = totalSelecionado();
  const saldo = orcamento - total;
  const estourou = saldo < 0;
  const porcentagem = Math.min((total / orcamento) * 100, 100);

  document.getElementById("valor-orcamento").textContent = moeda.format(orcamento);
  document.getElementById("valor-selecionado").textContent = moeda.format(total);

  const campoSaldo = document.getElementById("valor-saldo");
  campoSaldo.textContent = moeda.format(saldo);
  campoSaldo.classList.toggle("texto-alerta", estourou);
  campoSaldo.classList.toggle("texto-sucesso", !estourou);

  const barra = document.getElementById("barra-orcamento");
  barra.style.width = porcentagem + "%";
  barra.classList.toggle("barra-progresso__preenchimento--estourado", estourou);

  document.getElementById("resumo").classList.toggle("resumo-orcamento--estourado", estourou);
  document.getElementById("aviso-estouro").hidden = !estourou;
  document.getElementById("valor-estouro").textContent = moeda.format(-saldo);
}

function criarItem(atracao, textoBotao, aoClicar) {
  const modelo = document.getElementById("modelo-atracao");
  const item = modelo.content.firstElementChild.cloneNode(true);

  item.querySelector(".item-atracao__nome").textContent = atracao.nome;
  item.querySelector(".item-atracao__endereco").textContent = atracao.endereco || "Endereço não informado";
  item.querySelector(".item-atracao__categoria").textContent = nomesCategorias[atracao.categoria] || atracao.categoria;
  item.querySelector(".item-atracao__custo").textContent = moeda.format(Number(atracao.custo_estimado));

  const botao = item.querySelector(".item-atracao__botao");
  if (aoClicar) {
    botao.textContent = textoBotao;
    botao.addEventListener("click", () => aoClicar(atracao, botao));
  } else {
    botao.remove();
  }

  return item;
}

function mostrarRoteiro() {
  const lista = document.getElementById("lista-roteiro");
  lista.replaceChildren();

  selecionadas.forEach((atracao) => {
    const item = criarItem(atracao, "Remover", remover);
    item.querySelector(".item-atracao__botao").classList.add("btn--secundario");
    item.querySelector(".item-atracao__situacao").remove();
    lista.append(item);
  });

  document.getElementById("contador-roteiro").textContent = selecionadas.length;
  document.getElementById("roteiro-vazio").hidden = selecionadas.length > 0;
}

function mostrarSugestoes() {
  const lista = document.getElementById("lista-sugestoes");
  lista.replaceChildren();

  const saldo = orcamento - totalSelecionado();

  sugestoes.forEach((sugestao) => {
    const item = criarItem(sugestao, "Adicionar", adicionar);
    item.querySelector(".item-atracao__botao").classList.add("btn--acao");

    const cabe = Number(sugestao.custo_estimado) <= saldo;
    const situacao = item.querySelector(".item-atracao__situacao");
    situacao.textContent = cabe ? "Cabe no orçamento" : "Passa do orçamento";
    situacao.classList.add(cabe ? "etiqueta--verde" : "etiqueta--vermelha");

    lista.append(item);
  });
}

async function adicionar(sugestao, botao) {
  botao.disabled = true;

  try {
    const nova = await chamarApi("atracoes/", {
      method: "POST",
      body: JSON.stringify({
        nome: sugestao.nome,
        categoria: sugestao.categoria,
        custo_estimado: sugestao.custo_estimado,
        tempo_estimado_horas: sugestao.tempo_estimado_horas,
        endereco: sugestao.endereco,
        api_external_id: sugestao.api_external_id,
      }),
    });
    selecionadas.push(nova);
    sugestoes = sugestoes.filter((item) => item !== sugestao);
    atualizarTela();
  } catch (erro) {
    mostrarAviso(erro.message);
    botao.disabled = false;
  }
}

async function remover(atracao, botao) {
  botao.disabled = true;

  try {
    await chamarApi(`atracoes/${atracao.id}/`, { method: "DELETE" });
    selecionadas = selecionadas.filter((item) => item.id !== atracao.id);
    atualizarTela();
  } catch (erro) {
    mostrarAviso(erro.message);
    botao.disabled = false;
  }
}

async function buscarSugestoes(evento) {
  evento.preventDefault();

  const marcadas = [...formBusca.querySelectorAll("input:checked")].map((campo) => campo.value);
  if (marcadas.length === 0) {
    mostrarAviso("Escolha pelo menos uma categoria.");
    return;
  }

  botaoBusca.disabled = true;
  botaoBusca.textContent = "Buscando...";
  mostrarAviso("");

  try {
    const dados = await chamarApi("sugestoes/?categorias=" + encodeURIComponent(marcadas.join(",")));
    sugestoes = dados.sugestoes;

    if (dados.fonte === "local") {
      mostrarAviso(`Busca externa indisponível agora (${dados.aviso}). Mostrando atrações já salvas no sistema.`);
    } else if (sugestoes.length === 0) {
      mostrarAviso("Nenhuma atração encontrada para essas categorias.");
    }

    mostrarSugestoes();
  } catch (erro) {
    mostrarAviso(erro.message);
  } finally {
    botaoBusca.disabled = false;
    botaoBusca.textContent = "Buscar";
  }
}

function atualizarTela() {
  atualizarResumo();
  mostrarRoteiro();
  mostrarSugestoes();
}

formBusca.addEventListener("submit", buscarSugestoes);
atualizarTela();
