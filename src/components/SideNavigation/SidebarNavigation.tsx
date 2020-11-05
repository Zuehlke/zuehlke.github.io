import './SidebarNavigation.scss';
import React from 'react';
import {Link} from "react-router-dom";
import {MetaLinkSpec, RouteSpec, Runnable} from "../../common/types";
import {useDispatch, useSelector} from "react-redux";
import {SystemState} from "../../store/reducer";
import {StateActionFactory} from "../../store/actions";

type Props = {
  routes: RouteSpec[];
  metaLinks: MetaLinkSpec[];
  onNavigateCallback: Runnable;
}

const SidebarNavigation = (props: Props) => {

  const sidebarVisible = useSelector((state: SystemState) => state.sidebarNavVisible);
  const dispatch = useDispatch();

  const routeLink = (route: RouteSpec) => {
    return (
      <div className="link-container" onClick={() => handleLinkClicked(true)}>
        <Link to={route.to}>{route.display}</Link>
      </div>
    );
  }

  const metaNavLink = (link: MetaLinkSpec) => {
    return (
      <div className="link-container" onClick={() => handleLinkClicked(false)}>
        <a href={link.href} target="_blank" rel="noreferrer">{link.display}</a>
      </div>
    );
  }

  // Custom code in addition to route change.
  const handleLinkClicked = (mainNav: boolean) => {
    dispatch(StateActionFactory.hideSidebarNav());
    if (mainNav) {
      props.onNavigateCallback();
    }
  };

  return (
    <div className={`SidebarNavigation ${sidebarVisible ? "visible" : ""}`}>
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
