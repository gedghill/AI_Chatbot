import React from 'react';
// import '../styles/ProductSection.css';

const ProductSection = () => {
  const categories = [
    { name: 'Halloween Cakes' },
    { name: 'Birthday Cakes' },
    { name: 'Hampers' },
    { name: 'Occasions' },
    { name: 'Pies & Cheesecakes' },
    { name: 'Brownies & Cookies' },
    { name: 'Weddings' },
    { name: 'Cakes' },
    { name: 'Cupcakes' },
    { name: 'Cookies' },
];

  return (
    <div className="product-section">
      {categories.map((category, index) => (
        <div key={index} className="category-card">
          <h3>{category.name}</h3>
        </div>
      ))}
    </div>
  );
};

export default ProductSection;