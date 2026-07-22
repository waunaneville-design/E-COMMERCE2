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
