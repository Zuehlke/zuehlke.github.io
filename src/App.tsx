import React, {useRef, useState} from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import './App.scss';
import Hero from "./components/Hero/Hero";
import ZueBanner from "./components/ZueBanner/ZueBanner";
import Navigation from "./components/Navigation/Navigation";
import Footer from "./components/Footer/Footer";

import SidebarNavigation from "./components/SideNavigation/SidebarNavigation";
import {MetaLinkSpec, RepoSpec, RouteSpec} from "./common/types";
import OverlayStateContext, {OverlayState} from "./context/overlayState";
import Contributions from "./pages/Contributions/Contributions";

function App() {

  const pageContentRef = useRef<HTMLDivElement>(null);

  // Set up state for overlay context
  const [overlayState, setOverlayState] = useState<OverlayState>({
    sidebarNavVisible: false
  });

  const contributionRepos: RepoSpec[] = [
    {title: "Scenarioo", description: "Documentation tool to leverage the power of user interface tests by making them visible, understandable and useful for all (also non-technical) colleagues, that are involved in the software development process. Founded, driven and developed by a team of Zühlke engineers in collaboration with our customers and their needs.", url: "https://www.zuehlke.com/en"},
    {title: "quickstart-angular", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
    {title: "MvvmCross", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
    {title: "linux-developer-kitchen", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
    {title: "java-developer-vm", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
    {title: "linus-kitchen", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
    {title: "cookbook-windev", description: "Lorem ipsum", url: "https://www.zuehlke.com/en"},
  ];

  const routes = [
    {
      to: "/contributions",
      component: <Contributions repos={contributionRepos}/>,
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
const People = () => {
  return (
    <div className="placeholder">
      <div className="content">
        <h1>People</h1>
      </div>
    </div>
  )
}

export default App;
