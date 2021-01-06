import React, {useRef, useState} from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation from "./components/Navigation/Navigation";
import Footer from "./components/Footer/Footer";
import contributions from "./data/contributions.json";
import externalContributions from "./data/external_contributions.json";
import people from "./data/people.json";

import SidebarNavigation from "./components/SideNavigation/SidebarNavigation";
import {MetaLinkSpec, RouteSpec} from "./common/types";
import OverlayStateContext, {OverlayState} from "./context/overlayState";
import Contributions from "./pages/Contributions/Contributions";
import People from "./pages/People/People";

function App() {

  const pageContentRef = useRef<HTMLDivElement>(null);

  // Set up state for overlay context
  const [overlayState, setOverlayState] = useState<OverlayState>({
    sidebarNavVisible: false
  });

  const routes = [
    {
      to: "/contributions",
      component: <Contributions repos={contributions}
                                externalRepos={externalContributions}
                                displayedRepos={contributions.concat(externalContributions)}/>,
      display: "Contributions"
    },
    {
      to: "/people",
      component: <People people={people} displayedPeople={people}/>,
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
        <OverlayStateContext.Provider value={{overlayState, setOverlayState}}>
          <Navigation
            routes={routes}
            metaLinks={metaLinks}
            onNavigateCallback={scrollToPageContent}/>
          <SidebarNavigation
            routes={routes}
            metaLinks={metaLinks}
            onNavigateCallback={scrollToPageContent}/>
        </OverlayStateContext.Provider>

        { /* Content, blurred out when nav is open. */}
        <div className={`blurable ${overlayState.sidebarNavVisible ? "blur": ""}`}>
          <Hero/>
          { /* Main routable page content */}
          <div ref={pageContentRef}>
            <Switch>
              {routes.map((route) => (
                <Route key={route.display} path={route.to} exact>
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

export default App;
