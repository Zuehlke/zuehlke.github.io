import './Navigation.scss';
import React, {ReactNode} from 'react';
import {Link} from "react-router-dom";

export type RouteSpec = {
  to: string,
  component: ReactNode,
  display: string;
};

type MetaLinkSpec = {
  href: string;
  display: string;
};

type Props = {
  routes: RouteSpec[];
}

const Navigation = (props: Props) => {

  const metaLinks = [
    {href: "https://www.zuehlke.com", display: "Zühlke Website"},
    {href: "https://www.zuehlke.com/careers", display: "Careers"},
    {href: "https://www.zuehlke.com/insights", display: "Insights"}
  ] as MetaLinkSpec[]

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

  return (
    <header className="Navigation">
      <div className="content">
        <div className="branding-container">
          <div className="branding"/>
        </div>
        <div className="nav-links">
          <div className="meta-nav">
            { metaLinks.map((link: MetaLinkSpec) => metaNavLink(link)) }
          </div>
          <nav className="main-nav">
              { props.routes.map((route: RouteSpec) => routeLink(route)) }
          </nav>
        </div>
        <div className="hamburger-container">
          <button>Burger</button>
        </div>
      </div>
    </header>
  );
};

export default Navigation;
