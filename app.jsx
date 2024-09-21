import React from "react";
import "./App.css"
import Header from "./Header";
import HeroSection from "./HeroSection";
import ShopSection from "./ShopSection";
import Footer from "./Footer";

const App = () => {
  return (
    <div>
      <Header />
      <HeroSection />
      <ShopSection />
      <Footer />
    </div>
  );
};

export default App;
