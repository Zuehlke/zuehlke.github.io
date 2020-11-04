import './Navigation.scss';
import React, {useState} from 'react';
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {MetaLinkSpec, RouteSpec} from "../../common/types";

type Props = {
  routes: RouteSpec[];
  metaLinks: MetaLinkSpec[]
  onHamburgerClicked: () => void;
}

const Navigation = (props: Props) => {

  const [hamburgerActive, setHamburgerActive] = useState<boolean>(false);

  const metaNavLink = (link: MetaLinkSpec) => {
    return (
      <div className="link-container">
        <a href={link.href} target="_blank" rel="noreferrer">{link.display}</a>
      </div>
    );
  }

  const routeLink = (route: RouteSpec) => {
    return (
      <div className="link-container">
        <Link to={route.to}>{route.display}</Link>
      </div>
    );
  }

  const handleHamburgerClick = () => {
    setHamburgerActive(!hamburgerActive);
    props.onHamburgerClicked();
  }

  return (
    <header className="Navigation">
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
            {hamburgerActive ?
              <FontAwesomeIcon icon={["fas", "times"]}/> :
              <FontAwesomeIcon icon={["fas", "bars"]}/>}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navigation;
