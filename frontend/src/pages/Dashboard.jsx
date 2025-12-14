import { useEffect, useState } from "react";

function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export default function Dashboard({ token }) {
  const [sweets, setSweets] = useState([]);
  const [searchName, setSearchName] = useState("");

  // Admin form state
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");

  const user = parseJwt(token);
  const isAdmin = user?.is_admin;

  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  const fetchSweets = async () => {
    const res = await fetch(
      "http://127.0.0.1:8000/api/sweets",
      { headers }
    );
    const data = await res.json();
    setSweets(data);
  };

  const search = async () => {
    const res = await fetch(
      `http://127.0.0.1:8000/api/sweets/search?name=${searchName}`,
      { headers }
    );
    const data = await res.json();
    setSweets(data);
  };

  const purchase = async (id) => {
    await fetch(
      `http://127.0.0.1:8000/api/sweets/${id}/purchase`,
      { method: "POST", headers }
    );
    fetchSweets();
  };

  // 🔐 ADMIN ACTIONS

  const addSweet = async () => {
    const res = await fetch(
      "http://127.0.0.1:8000/api/sweets",
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          name,
          category,
          price: Number(price),
          quantity: Number(quantity),
        }),
      }
    );

    if (!res.ok) {
      alert("Failed to add sweet");
      return;
    }

    setName("");
    setCategory("");
    setPrice("");
    setQuantity("");
    fetchSweets();
  };

  const deleteSweet = async (id) => {
    await fetch(
      `http://127.0.0.1:8000/api/sweets/${id}`,
      {
        method: "DELETE",
        headers,
      }
    );
    fetchSweets();
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  return (
  <div className="container">
    <div className="header">
      <h2>Welcome to Kata Sweets Shop</h2>
      <button
        className="secondary"
        onClick={() => {
          localStorage.removeItem("token");
          window.location.reload();
        }}
      >
        Logout
      </button>
    </div>

    {/* SEARCH */}
    <div className="card">
      <input
        placeholder="Search sweets by name"
        value={searchName}
        onChange={(e) => setSearchName(e.target.value)}
      />
      <button onClick={search}>Search</button>
    </div>

    {/* ADMIN PANEL */}
    {isAdmin && (
      <div className="admin-panel card">
        <h3>Admin Panel</h3>

        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
        <input placeholder="Price" type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
        <input placeholder="Quantity" type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} />

        <button onClick={addSweet}>Add Sweet</button>
      </div>
    )}

    {/* SWEETS */}
    {sweets.map((s) => (
      <div className="card" key={s.id}>
        <h4>{s.name}</h4>
        <p>Category: {s.category}</p>
        <p>Price: ₹{s.price}</p>
        <p>Available: {s.quantity}</p>

        <button disabled={s.quantity === 0} onClick={() => purchase(s.id)}>
          Purchase
        </button>

        {isAdmin && (
          <button
            className="secondary"
            onClick={() => deleteSweet(s.id)}
            style={{ marginLeft: 10 }}
          >
            Delete
          </button>
        )}
      </div>
    ))}
  </div>
);
}