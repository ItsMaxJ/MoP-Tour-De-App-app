(function () {
  const tableContainer = document.getElementById("product-list");
  let editingId = null;

  const { setEditing, resetForm } = initProductForm({
    onSubmit: async ({ id, name, cost }) => {
      if (id !== null) {
        await updateProduct(id, { name, cost });
        resetForm();
        editingId = null;
      } else {
        await createProduct({ name, cost });
      }
      loadProducts();
    },
  });

  async function loadProducts() {
    try {
      const data = await getProducts();
      renderProductTable(tableContainer, data, {
        onEdit: (product) => {
          editingId = product.id;
          setEditing(product);
        },
        onDelete: async (id) => {
          await deleteProduct(id);
          if (editingId === id) {
            resetForm();
            editingId = null;
          }
          loadProducts();
        },
      });
    } catch (e) {
      console.error("Failed to load products:", e);
    }
  }

  loadProducts();
})();
