import React from 'react';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Footer from "./components/Footer/Footer";

import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
library.add(fab)

function App() {
  return (
    <div className="App">
      <Hero/>
      <ZueBanner/>
      <Footer/>
    </div>
  );
}

export default App;
