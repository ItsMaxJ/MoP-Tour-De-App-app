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

async function getStops() {
  const res = await fetch(`${API_URL}/v1/stops`);
  return res.json();
}

async function createStop(stop) {
  const res = await fetch(`${API_URL}/v1/stops`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(stop),
  });
  return res.json();
}

async function updateStop(id, stop) {
  const res = await fetch(`${API_URL}/v1/stops/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(stop),
  });
  if (res.status === 404) {
    const err = await res.json();
    throw new Error(err.message);
  }
  return res.json();
}

async function deleteStop(id) {
  const res = await fetch(`${API_URL}/v1/stops/${id}`, {
    method: "DELETE",
  });
  if (res.status == 404) {
    throw new Error(`Delete failed: 404`);
  }
}

async function getStop(id) {
  const res = await fetch(`${API_URL}/v1/stops/${id}`);
  return res.json();
}
