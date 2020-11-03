import './Footer.scss';
import React from 'react';
import logo from '../../assets/images/logo/logo-zuehlke-big.png'

const Footer = () => {
  return (
    <div className="Footer">
      <div className="content">
        <div className="logo">
          <a href="https://www.zuehlke.com/en" target="_blank"><img src={logo} /></a>
        </div>
        <div className="links">
          <ul>
            <li><a href="https://www.zuehlke.com/en/our-expertise" target="_blank">Our Expertise</a></li>
            <li><a href="https://www.zuehlke.com/en/our-projects" target="_blank">Our Projects</a></li>
            <li><a href="https://www.zuehlke.com/en/insights" target="_blank">Our Insights</a></li>
            <li><a href="https://www.zuehlke.com/en/about-us" target="_blank">About us</a></li>
            <li><a href="https://www.zuehlke.com/en/careers" target="_blank">Careers</a></li>
            <li><a href="https://www.zuehlke.com/en/legal-notice" target="_blank">Legal</a></li>
            <li><a href="https://www.zuehlke.com/en/privacy-policy" target="_blank">Terms of Use & Data Privacy</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Footer;
