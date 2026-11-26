document.querySelectorAll(".grafico-barras__barra").forEach((barra) => {
  barra.style.width = barra.dataset.porcentagem + "%";
});

document.getElementById("botao-imprimir").addEventListener("click", () => window.print());
