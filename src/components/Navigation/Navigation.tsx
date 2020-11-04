import './Navigation.scss';
import React from 'react';
import {NavLinkSpec} from "../../navLinks";

type Props = {
  metaNavLinks: NavLinkSpec[];
  mainNavLinks: NavLinkSpec[];
}

const Navigation = (props: Props) => {
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
                .map((link: NavLinkSpec) => <a href={link.target}>{link.value}</a>)
            }
          </div>
          <nav className="main-nav">
            {
              props.mainNavLinks
                .map((link: NavLinkSpec) => <a href={link.target}>{link.value}</a>)
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
