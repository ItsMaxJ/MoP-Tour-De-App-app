const API_URL = "http://localhost:3001/api";

async function getProducts() {
  const res = await fetch(`${API_URL}/product`);
  return res.json();
}

async function createProduct(product) {
  const res = await fetch(`${API_URL}/product`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  return res.json();
}

async function updateProduct(id, product) {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (res.status === 404) {
    const err = await res.json();
    throw new Error(err.message);
  }
  return res.json();
}

async function deleteProduct(id) {
  const res = await fetch(`${API_URL}/product/${id}`, {
    method: "DELETE",
  });
  return res.json();
}
async function checkHealth() {
  const res = await fetch(`${API_URL}/health`);
  return res.json()
}
