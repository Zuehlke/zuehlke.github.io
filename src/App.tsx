import React from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation, {RouteSpec} from "./components/Navigation/Navigation";
import Footer from "./components/Footer/Footer";

import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
library.add(fab)

function App() {

  const routes = [
    {
      to: "/contributions",
      component: <Contributions/>,
      display: "Contributions"
    },
    {
      to: "/people",
      component: <People/>,
      display: "People"
    },
  ] as RouteSpec[];

  const defaultRoute = routes[0];

  return (
    <div className="App">
      <Router>
        <Navigation routes={routes}/>
        <Hero/>

        {/* Routable content */}
        <Switch>
          {routes.map((route) => (
            <Route path={route.to} exact>
              {route.component}
            </Route>
          ))}
          <Route path="/" exact>
            {defaultRoute.component}
          </Route>
        </Switch>

        <ZueBanner/>
        <Footer/>
      </Router>
    </div>
  );
}

// Placeholders for routable components
// TODO: Remove these when replaced with actual components.
const Contributions = () => {
  return <h1>Contributions</h1>
}

const People = () => {
  return <h1>People</h1>
}

export default App;
