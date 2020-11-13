import './SidebarNavigation.scss';
import React, {useContext} from 'react';
import {Link} from "react-router-dom";
import {MetaLinkSpec, RouteSpec, Runnable} from "../../common/types";
import OverlayStateContext from "../../context/overlayState";

type Props = {
  routes: RouteSpec[];
  metaLinks: MetaLinkSpec[];
  onNavigateCallback: Runnable;
}

const SidebarNavigation = (props: Props) => {

  const {overlayState, setOverlayState} = useContext(OverlayStateContext);

  const routeLink = (route: RouteSpec) => {
    return (
      <div key={route.to} className="link-container" onClick={() => handleLinkClicked(true)}>
        <Link to={route.to}>{route.display}</Link>
      </div>
    );
  }

  const metaNavLink = (link: MetaLinkSpec) => {
    return (
      <div key={link.href} className="link-container" onClick={() => handleLinkClicked(false)}>
        <a href={link.href} target="_blank" rel="noreferrer">{link.display}</a>
      </div>
    );
  }

  // Custom code in addition to route change.
  const handleLinkClicked = (mainNav: boolean) => {
    setOverlayState({
      ...overlayState,
      sidebarNavVisible: false
    })
    if (mainNav) {
      props.onNavigateCallback();
    }
  };

  return (
    <div className={`SidebarNavigation ${overlayState.sidebarNavVisible ? "visible" : ""}`}>
      <div className="content">
        <div className="nav-links">
          <nav className="main-nav">
            {props.routes.map((route: RouteSpec) => routeLink(route))}
          </nav>
          <div className="meta-nav">
            {props.metaLinks.map((link: MetaLinkSpec) => metaNavLink(link))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SidebarNavigation;
