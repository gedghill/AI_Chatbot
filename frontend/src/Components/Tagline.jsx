import React, { useState } from 'react';
import axios from 'axios';

const Tagline = () => {
  const [orderName, setOrderName] = useState('');

  const placeOrder = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/order', { name: orderName });
      alert(response.data.message);
    } catch (error) {
      alert('Failed to place order');
    }
  };

  return (
    <div className="text-center py-10 px-4 bg-pink-50 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold mb-6 text-pink-500">
        Delicious Desserts for Every Occasion
      </h1>
      <div className="flex flex-col items-center gap-4">
        <input
          type="text"
          placeholder="Your Name"
          value={orderName}
          onChange={(e) => setOrderName(e.target.value)}
          className="p-3 w-full max-w-xs border rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
        />
        <button
          onClick={placeOrder}
          className="bg-pink-500 text-white px-6 py-3 rounded-md font-bold hover:bg-pink-600 transition duration-300"
        >
          Order Now
        </button>
      </div>
    </div>
  );
};

export default Tagline;
