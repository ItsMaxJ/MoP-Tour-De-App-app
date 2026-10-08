function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function renderProductTable(container, products, { onEdit, onDelete }) {
  if (products.length === 0) {
    container.innerHTML = "<p>No products.</p>";
    return;
  }

  const table = document.createElement("table");
  table.innerHTML = `
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Cost</th>
        <th>Actions</th>
      </tr>
    </thead>`;

  const tbody = document.createElement("tbody");

  for (const p of products) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p.id}</td>
      <td>${escapeHtml(p.name)}</td>
      <td>${p.cost}</td>
      <td class="actions"></td>`;

    const actions = tr.querySelector(".actions");

    const btnEdit = document.createElement("button");
    btnEdit.textContent = "Edit";
    btnEdit.addEventListener("click", () => onEdit(p));

    const btnDelete = document.createElement("button");
    btnDelete.textContent = "Delete";
    btnDelete.addEventListener("click", () => onDelete(p.id));

    actions.append(btnEdit, btnDelete);
    tbody.appendChild(tr);
  }

  table.appendChild(tbody);
  container.replaceChildren(table);
}
