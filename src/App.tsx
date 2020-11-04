import React from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation from "./components/Navigation/Navigation";
import Footer from "./components/Footer/Footer";

import SidebarNavigation from "./components/SideNavigation/SidebarNavigation";
import {MetaLinkSpec, RouteSpec} from "./common/types";

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

  const metaLinks = [
    {href: "https://www.zuehlke.com", display: "Zühlke Website"},
    {href: "https://www.zuehlke.com/careers", display: "Careers"},
    {href: "https://www.zuehlke.com/insights", display: "Insights"}
  ] as MetaLinkSpec[]

  return (
    <div className="App">
      <Router>
        <Navigation
          routes={routes}
          metaLinks={metaLinks}/>
        <SidebarNavigation
          routes={routes}
          metaLinks={metaLinks}/>
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
