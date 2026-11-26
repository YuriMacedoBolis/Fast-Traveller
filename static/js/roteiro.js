const roteiro = document.getElementById("roteiro");
const orcamento = Number(roteiro.dataset.orcamento);
const nomesCategorias = JSON.parse(document.getElementById("dados-categorias").textContent);
const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

let selecionadas = JSON.parse(document.getElementById("dados-atracoes").textContent);

function totalSelecionado() {
  return selecionadas.reduce((soma, atracao) => soma + Number(atracao.custo_estimado), 0);
}

function atualizarResumo() {
  const total = totalSelecionado();
  const saldo = orcamento - total;

  document.getElementById("valor-orcamento").textContent = moeda.format(orcamento);
  document.getElementById("valor-selecionado").textContent = moeda.format(total);
  document.getElementById("valor-saldo").textContent = moeda.format(saldo);
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
    const item = criarItem(atracao);
    item.querySelector(".item-atracao__situacao").remove();
    lista.append(item);
  });

  document.getElementById("contador-roteiro").textContent = selecionadas.length;
  document.getElementById("roteiro-vazio").hidden = selecionadas.length > 0;
}

function atualizarTela() {
  atualizarResumo();
  mostrarRoteiro();
}

atualizarTela();
