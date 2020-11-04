import './Navigation.scss';
import React from 'react';
import {NavLinkSpec} from "../../navLinks";

type Props = {
  metaNavLinks: NavLinkSpec[];
  mainNavLinks: NavLinkSpec[];
}

const Navigation = (props: Props) => {

  const metaNavLink = (spec: NavLinkSpec) => {
    return (
      <div className="link-container">
        <a href={spec.href} target="_blank" rel="noreferrer">{spec.display}</a>
      </div>
    );
  }

  const mainNavLink = (spec: NavLinkSpec) => {
    return <div className="link-container"><a href={spec.href}>{spec.display}</a></div>;
  }

  return (
    <header className="Navigation">
      <div className="content">
        <div className="branding-container">
          <div className="branding"/>
        </div>
        <div className="nav-links">
          <div className="meta-nav">
            {
              props.metaNavLinks
                .map((spec: NavLinkSpec) => metaNavLink(spec))
            }
          </div>
          <nav className="main-nav">
            {
              props.mainNavLinks
                .map((spec: NavLinkSpec) => mainNavLink(spec))
            }
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
