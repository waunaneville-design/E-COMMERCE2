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

