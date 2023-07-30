import React, { useState } from 'react';
import axios from 'axios';
import backgroundImage from './Bill.jpg'; 
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [clients, setClients] = useState([]);
  const [sales, setSales] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [setIsSearchTriggered] = useState(false); 

  const handleSearch = async () => {
    setIsSearchTriggered(true); 
    try {
      const response = await axios.get(`http://localhost:8000/client/${inputValue}`);
      setClients(response.data);
      setSelectedClient(null);
      setSales([]);
    } catch (error) {
      console.error(error);
    }
  };

  const handleClientClick = async (client) => {
    setSelectedClient(client);
    try {
      const response = await axios.get(`http://localhost:8000/sales/${client.customers_id}`);
      setSales(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}  className="center-content">
      <img src={backgroundImage} alt="background" style={{width: '100%', height: '40vh', objectFit: 'cover'}} />

      <h1 style={{ textAlign: "center" }}>Apprenticeship - Test technique Full-Stack</h1>

      <input className="input" placeholder='Entrez un nom (ex: Dupont)' value={inputValue} onChange={e => setInputValue(e.target.value)} />
      <button className="button"onClick={handleSearch}>Rechercher</button>

      <h1>Résultats de recherche :</h1>
      {/* {isSearchTriggered && clients.length === 0 && <p>Aucun client trouvé avec ce nom.</p>} */}
      <ul>
        {clients.map(client => (
          <li key={client.customers_id} className="client" onClick={() => handleClientClick(client)}>
            <div><strong>Nom :</strong> {client.last_name}</div>
            <div><strong>Prenom :</strong> {client.first_name}</div>
            <div><strong>Email :</strong> {client.email}</div>
            <div><strong>Phone :</strong> {client.phone}</div>
          </li>
        ))}
      </ul>

      {selectedClient && (
        <>
          <h1>Ventes du client {selectedClient.last_name} {selectedClient.first_name} :</h1>
          <ul>
            {sales.map((sale, index) => (
              <li key={sale.sale_id} className="vente" style={{ marginBottom: "10px" }}>
                <h3>Vente {index + 1} :</h3>
                <div><strong>ID de la vente :</strong> {sale.sale_id}</div>
                <div><strong>Créé le :</strong> {sale.created_at}</div>
                <div><strong>Complété le :</strong> {sale.completed_at}</div>
                <div><strong>Date Z :</strong> {sale.date_z}</div>
                <div><strong>ID du magasin :</strong> {sale.store_id}</div>
                <div><strong>ID du vendeur :</strong> {sale.vendor_id}</div>
                <div><strong>ID de vente unique :</strong> {sale.unique_sale_id}</div>
                <div><strong>ID du client :</strong> {sale.customer_id}</div>
                <div><strong>Devise :</strong> {sale.currency}</div>
                <div><strong>Total :</strong> {sale.total}</div>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
