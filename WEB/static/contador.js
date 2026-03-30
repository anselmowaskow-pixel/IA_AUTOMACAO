let documentos = [];

fetch("http://127.0.0.1:5001/api/contador/documentos")
.then(r => r.json())
.then(dados => {
  documentos = dados;
  render(dados);
});

function render(lista) {
  const tbody = document.querySelector("#tabela tbody");
  tbody.innerHTML = "";
  lista.forEach(d => {
    const tr = document.createElement("tr");
    if (d.status === "OK") tr.className = "ok";
    else if (d.status === "ERRO") tr.className = "erro";
    else tr.className = "aviso";

    tr.innerHTML = `
      <td>${d.entidade}</td>
      <td>${d.arquivo}</td>
      <td>${d.tipo_documento}</td>
      <td>${d.status}</td>
      <td>${d.data}</td>
      <td>${d.origem}</td>
      <td>
        <button onclick="alert('Auditar')">Auditar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filtrar() {
  const q = document.getElementById("busca").value.toLowerCase();
  render(documentos.filter(d =>
    d.arquivo.toLowerCase().includes(q) ||
    d.entidade.toLowerCase().includes(q)
  ));
}