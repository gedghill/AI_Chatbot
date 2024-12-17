import React from 'react';

const NavigationBar = () => {
  return (
    <nav className="fixed top-0 left-0 w-full bg-pink-100 shadow-md z-10">
      <div className="container mx-auto flex justify-between items-center p-4">
        {/* Brand Logo */}
        <div className="navbar-brand">
          <a href="#">
            <img src="/images/1.png" alt="Logo" className="h-10 w-auto" />
          </a>
        </div>

        {/* Bakery Name */}
        <div className="text-2xl font-bold text-pink-600">
         Welcome to The Tipsy Boutique
        </div>

        {/* Navigation Links */}
        <div className="flex space-x-4">
          <a href="#" className="p-2 rounded-full hover:bg-pink-300 focus:bg-pink-400 transition duration-300">
            <img src="/images/search.png" alt="Search" className="h-8 w-8" />
          </a>
          <a href="#" className="p-2 rounded-full hover:bg-pink-300 focus:bg-pink-400 transition duration-300">
            <img src="/images/store.png" alt="Stores" className="h-8 w-8" />
          </a>
          <a href="#" className="p-2 rounded-full hover:bg-pink-300 focus:bg-pink-400 transition duration-300">
            <img src="/images/user.png" alt="Profile" className="h-8 w-8" />
          </a>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;
