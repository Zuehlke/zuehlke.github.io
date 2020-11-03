import React from 'react';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation from "./components/Navigation/Navigation";
import navLinks from "./navLinks";

function App() {
  return (
    <div className="App">
      <Navigation mainNavLinks={navLinks.main} metaNavLinks={navLinks.meta}/>
      <Hero/>
      <ZueBanner/>
    </div>
  );
}

export default App;
