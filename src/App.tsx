import React from 'react';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";

function App() {
  return (
    <div className="App">
      <Hero/>
      <ZueBanner/>
    </div>
  );
}

export default App;
