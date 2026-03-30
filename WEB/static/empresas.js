async function carregar() {
    const resp = await fetch("/api/status");
    const dados = await resp.json();
  
    const tbody = document.getElementById("tabela");
    tbody.innerHTML = "";
  
    Object.keys(dados).forEach(entidade => {
      const info = dados[entidade];
  
      const tr = document.createElement("tr");
  
      tr.innerHTML = `
        <td>${entidade}</td>
        <td class="${info.status || ''}">${info.status || ''}</td>
        <td>${info.etapa_atual || ''}</td>
        <td>${info.documentos_ok || 0}</td>
        <td>${info.documentos_erro || 0}</td>
        <td>${info.ultima_atualizacao || ''}</td>
        <td>
          <button onclick="verEventos('${entidade}')">Ver eventos</button>
        </td>
      `;
  
      tbody.appendChild(tr);
    });
  }
  
  function verEventos(entidade) {
    window.open(`/api/eventos/${entidade}`, "_blank");
  }
  
  carregar();