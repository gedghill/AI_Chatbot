import React from 'react';
import NavigationBar from './Components/NavigationBar';
import Banner from './Components/Banner';
import ProductSection from './Components/ProductSection';
import Tagline from './Components/Tagline';
import Chatbot from './Components/Chatbot';

function App() {
  return (
    <div className="bg-white min-h-screen">
      <NavigationBar />
      <div className="mt-16">
        <div className="mb-8">
          <Banner />
        </div>
        <div className="mb-8">
          <Tagline />
        </div>
        <div className="mb-8">
          {/* <ProductSection /> */}
        </div>
        <div className="fixed bottom-4 right-4">
          <Chatbot />
        </div>
      </div>
    </div>
  );
}

export default App;
