function initProductForm({ onSubmit }) {
  const form = document.getElementById("product-form");
  const inputName = document.getElementById("input-name");
  const inputCost = document.getElementById("input-cost");
  const btnSubmit = document.getElementById("btn-submit");
  const btnCancel = document.getElementById("btn-cancel");

  let editingId = null;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = inputName.value.trim();
    const cost = Number(inputCost.value);
    if (!name || !cost) return;

    onSubmit({ id: editingId, name, cost });

    if (!editingId) {
      form.reset();
    }
  });

  btnCancel.addEventListener("click", () => {
    resetForm();
  });

  function setEditing(product) {
    editingId = product.id;
    inputName.value = product.name;
    inputCost.value = product.cost;
    btnSubmit.textContent = "Save";
    btnCancel.style.display = "";
  }

  function resetForm() {
    editingId = null;
    form.reset();
    btnSubmit.textContent = "Add";
    btnCancel.style.display = "none";
  }

  return { setEditing, resetForm };
}
