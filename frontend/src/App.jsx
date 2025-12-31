import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import HomeScreen from './pages/HomeScreen';
import PriceTrend from './pages/PriceTrend';
import MarketDetail from './pages/MarketDetail';

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <div className="app">
          <Routes>
            <Route path="/" element={<HomeScreen />} />
            <Route path="/trend/:commodityId" element={<PriceTrend />} />
            <Route path="/market/:marketId" element={<MarketDetail />} />
          </Routes>
        </div>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
