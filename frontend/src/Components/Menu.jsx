import React from 'react';

const Menu = () => {
  const categories = ['Halloween Cakes', 'Birthday Cakes', 'Cakes', 'Cup Cakes', 'Pies and Cheesecakes', 'Brownies and Cookies', 'Weddings'];

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around', padding: '1rem', backgroundColor: '#f4f4f4' }}>
      {categories.map((category, index) => (
        <div key={index} style={{ padding: '1rem', cursor: 'pointer', fontWeight: 'bold' }}>
          {category}
        </div>
      ))}
    </div>
  );
};

export default Menu;
