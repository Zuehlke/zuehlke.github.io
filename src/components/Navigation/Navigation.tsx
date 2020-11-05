import './Navigation.scss';
import React, {useContext} from 'react';
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {MetaLinkSpec, RouteSpec, Runnable} from "../../common/types";
import OverlayStateContext from "../../context/overlayState";

type Props = {
  routes: RouteSpec[];
  metaLinks: MetaLinkSpec[],
  onNavigateCallback: Runnable,
}

const Navigation = (props: Props) => {

  // Global state
  const {overlayState, setOverlayState} = useContext(OverlayStateContext);

  const metaNavLink = (link: MetaLinkSpec) => {
    return (
      <div className="link-container">
        <a href={link.href} target="_blank" rel="noreferrer">{link.display}</a>
      </div>
    );
  }

  const routeLink = (route: RouteSpec) => {
    return (
      <div className="link-container" onClick={handleNavigate}>
        <Link to={route.to}>{route.display}</Link>
      </div>
    );
  }

  const handleHamburgerClick = () => {
    setOverlayState({
      ...overlayState,
      sidebarNavVisible: !overlayState.sidebarNavVisible
    })
  }

  const handleNavigate = () => {
    props.onNavigateCallback();
  };

  return (
    <header className={`Navigation ${overlayState.sidebarNavVisible ? "opaque" : ""}`}>
      <div className="content">
        <div className="branding-container">
          <div className="branding"/>
        </div>
        <div className="nav-links">
          <div className="meta-nav">
            {props.metaLinks.map((link: MetaLinkSpec) => metaNavLink(link))}
          </div>
          <nav className="main-nav">
            {props.routes.map((route: RouteSpec) => routeLink(route))}
          </nav>
        </div>
        <div className="hamburger-container">
          <button onClick={handleHamburgerClick} className="hamburger">
            {overlayState.sidebarNavVisible ?
              <FontAwesomeIcon icon={["fas", "times"]}/> :
              <FontAwesomeIcon icon={["fas", "bars"]}/>}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navigation;
