import './SidebarNavigation.scss';
import React from 'react';
import {Link} from "react-router-dom";
import {MetaLinkSpec, RouteSpec} from "../../common/types";

type Props = {
  routes: RouteSpec[];
  metaLinks: MetaLinkSpec[];
  visible: boolean;
  onHideSidebar: () => void;
}

const SidebarNavigation = (props: Props) => {

  const routeLink = (route: RouteSpec) => {
    return (
      <div className="link-container" onClick={handleLinkClicked}>
        <Link to={route.to}>{route.display}</Link>
      </div>
    );
  }

  const metaNavLink = (link: MetaLinkSpec) => {
    return (
      <div className="link-container" onClick={handleLinkClicked}>
        <a href={link.href} target="_blank" rel="noreferrer">{link.display}</a>
      </div>
    );
  }

  // Custom code in addition to route change.
  const handleLinkClicked = () => {
    props.onHideSidebar();
  };

  return (
    <div className={`SidebarNavigation ${props.visible ? "visible" : ""}`}>
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
