const { useEffect, useState } = React;

const emptyForm = {
  product_name: '',
  brands: '',
  barcode: '',
  ingredients_text: '',
  price: '',
  stock: '',
};

function App() {
  const [items, setItems] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState(emptyForm);
  const [status, setStatus] = useState({ text: 'Ready to add a new item.', isError: false });
  const [fetchForm, setFetchForm] = useState({ barcode: '', name: '' });
  const [fetchResult, setFetchResult] = useState('Use the form above to enrich inventory data with live product information.');

const loadInventory = async () => {
    try {
      const response = await fetch('/inventory');
      if (!response.ok) throw new Error('Unable to load inventory');
      setItems(await response.json());
    } catch (error) {
      setStatus({ text: error.message, isError: true });
    }
  };

useEffect(() => {
    loadInventory();
  }, []);

  const resetForm = () => {
    setFormData(emptyForm);
    setEditingId(null);
  };

   const handleInputChange = ({ target }) => {
    setFormData((prev) => ({ ...prev, [target.name]: target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = {
      product_name: formData.product_name.trim(),
      brands: formData.brands.trim(),
      barcode: formData.barcode.trim(),
      ingredients_text: formData.ingredients_text.trim(),
      price: Number(formData.price || 0),
      stock: Number(formData.stock || 0),
    };

    try {
      const response = editingId
        ? await fetch(`/inventory/${editingId}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        : await fetch('/inventory', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });

 if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Unable to save item');
      }

      
        setStatus({ text: editingId ? 'Item updated successfully.' : 'Item created successfully.', isError: false });
      resetForm();
      await loadInventory();
    } catch (error) {
      setStatus({ text: error.message, isError: true });
    }
  };

   const handleEdit = async (id) => {
    try {
      const response = await fetch(`/inventory/${id}`);
      if (!response.ok) throw new Error('Item not found');
      const item = await response.json();
      setEditingId(item.id);
      setFormData({
        product_name: item.product_name || '',
        brands: item.brands || '',
        barcode: item.barcode || '',
        ingredients_text: item.ingredients_text || '',
        price: item.price ?? '',
        stock: item.stock ?? '',
      });
      setStatus({ text: `Editing item ${item.id}.`, isError: false });
    } catch (error) {
      setStatus({ text: error.message, isError: true });
    }
    };

    const handleDelete = async (id) => {
    try {
      const response = await fetch(`/inventory/${id}`, { method: 'DELETE' });
      if (!response.ok) throw new Error('Unable to delete item');
      setStatus({ text: 'Item deleted successfully.', isError: false });
      await loadInventory();
    } catch (error) {
      setStatus({ text: error.message, isError: true });
    }
  };

const handleFetch = async () => {
    const barcode = fetchForm.barcode.trim();
    const name = fetchForm.name.trim();

    try {
      const params = new URLSearchParams();
      if (barcode) params.append('barcode', barcode);
      if (name) params.append('name', name);

 const response = await fetch(`/inventory/fetch?${params.toString()}`);
      if (!response.ok) throw new Error('No product found');
      const data = await response.json();
      setFetchResult(JSON.stringify(data, null, 2));

       if (data.product) {
        setFormData((prev) => ({
          ...prev,
          product_name: data.product.product_name || prev.product_name,
          brands: data.product.brands || prev.brands,
          barcode: data.product.barcode || prev.barcode,
          ingredients_text: data.product.ingredients_text || prev.ingredients_text,
        }));
        setStatus({ text: 'Product details loaded.', isError: false });
      }
    } catch (error) {
      setFetchResult(error.message);
      setStatus({ text: error.message, isError: true });
    }
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">E-commerce Operations</p>
          <h1>Inventory Administrator Portal</h1>
          <p className="subtitle">Manage stock, update product details, and enrich records with live product data.</p>
        </div>
      </header>

      <main className="grid">
        <section className="card">
          <div className="card-header">
            <h2>Inventory Item Form</h2>
            <p className="status" style={{ color: status.isError ? '#dc2626' : '#64748b' }}>{status.text}</p>
          </div>
          <form className="form-grid" onSubmit={handleSubmit}>
            <input type="hidden" value={editingId || ''} />
            <label>
              Product Name
              <input name="product_name" required placeholder="Enter product name" value={formData.product_name} onChange={handleInputChange} />
            </label>
            <label>
              Brand
              <input name="brands" placeholder="Brand name" value={formData.brands} onChange={handleInputChange} />
            </label>
            <label>
              Barcode
              <input name="barcode" placeholder="Barcode" value={formData.barcode} onChange={handleInputChange} />
            </label>
            <label>
              Ingredients
              <input name="ingredients_text" placeholder="Ingredients" value={formData.ingredients_text} onChange={handleInputChange} />
            </label>
            <label>
              Price
              <input name="price" type="number" step="0.01" min="0" placeholder="0.00" value={formData.price} onChange={handleInputChange} />
            </label>
            <label>
              Stock
              <input name="stock" type="number" min="0" placeholder="0" value={formData.stock} onChange={handleInputChange} />
            </label>
            <div className="form-actions">
              <button type="submit" className="primary">Save Item</button>
              <button type="button" className="secondary" onClick={resetForm}>Cancel</button>
            </div>
          </form>
        </section>

        <section className="card">
          <div className="card-header">
            <h2>Fetch Product Details</h2>
          </div>
          <div className="form-grid compact">
            <label>
              Barcode
              <input name="fetchBarcode" placeholder="Example: 1234567890123" value={fetchForm.barcode} onChange={(event) => setFetchForm((previous) => ({ ...previous, barcode: event.target.value }))} />
            </label>
            <label>
              Product Name
              <input name="fetchName" placeholder="Example: milk" value={fetchForm.name} onChange={(event) => setFetchForm((previous) => ({ ...previous, name: event.target.value }))} />
            </label>
            <div className="form-actions">
              <button type="button" className="primary" onClick={handleFetch}>Fetch</button>
            </div>
          </div>
          <pre className="result-box">{fetchResult}</pre>
        </section>
      </main>

  <section className="card">
        <div className="card-header">
          <h2>Current Inventory</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Brand</th>
                <th>Barcode</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan="7">No inventory items yet.</td>
                </tr>
              ) : (
                items.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.product_name || 'Unnamed'}</td>
                    <td>{item.brands || '-'}</td>
                    <td>{item.barcode || '-'}</td>
                    <td>${Number(item.price || 0).toFixed(2)}</td>
                    <td>{item.stock ?? 0}</td>
                    <td>
                      <button className="secondary" type="button" onClick={() => handleEdit(item.id)}>Edit</button>
                      <button className="danger" type="button" onClick={() => handleDelete(item.id)}>Delete</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);

