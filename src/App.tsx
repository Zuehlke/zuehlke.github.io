import React, {useRef} from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation from "./components/Navigation/Navigation";
import Footer from "./components/Footer/Footer";

import SidebarNavigation from "./components/SideNavigation/SidebarNavigation";
import {MetaLinkSpec, RouteSpec} from "./common/types";
import {useSelector} from "react-redux";
import {SystemState} from "./store/reducer";

function App() {

  const sidebarVisible = useSelector((state: SystemState) => state.sidebarNavVisible);
  const pageContentRef = useRef<HTMLDivElement>(null);

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

  const scrollToPageContent = () => {
    // Reset scroll to 0.
    window.scrollTo(0, 0);

    // If header or page element doesn't exist, abort here.
    const element = pageContentRef.current;
    const header = document.querySelector("header");
    if (!(element && header)) {
      return;
    }

    // Find y position of page content and height of header, scroll to
    // computed position.
    const pageY = element.getBoundingClientRect().y;
    const paddingTop: number = header.getBoundingClientRect().height;
    window.scrollTo(0, pageY - paddingTop);
  };

  return (
    <div className="App">
      <Router>
        <Navigation
          routes={routes}
          metaLinks={metaLinks}
          onNavigateCallback={scrollToPageContent}/>
        <SidebarNavigation
          routes={routes}
          metaLinks={metaLinks}
          onNavigateCallback={scrollToPageContent}/>

        <div className={sidebarVisible ? "blur" : ""}>
          <Hero/>

          <div ref={pageContentRef}>
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
          </div>

          <ZueBanner/>
          <Footer/>
        </div>


      </Router>
    </div>
  );
}

// Placeholders for routable components
// TODO: Remove these when replaced with actual components.
const Contributions = () => {
  return <div style={{height: "400px"}}><h1>Contributions</h1></div>
}

const People = () => {
  return <div style={{height: "400px"}}><h1>People</h1></div>
}

export default App;
