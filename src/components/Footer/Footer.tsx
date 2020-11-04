import './Footer.scss';
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
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
        <div className="stay-in-touch">
            <div className="row">
                Stay in touch
            </div>
            <div className="row">
                <div className="col">
                    <a href="https://www.linkedin.com/company/zuehlkegroup/" target="_blank"><FontAwesomeIcon icon={['fab', 'linkedin']} /></a>
                    <a href="https://github.com/Zuehlke" target="_blank"><FontAwesomeIcon icon={['fab', 'github']} /></a>
                </div>
                <div className="col">
                    <a href="https://www.facebook.com/zuehlke.group" target="_blank"><FontAwesomeIcon icon={['fab', 'facebook-square']} /></a>
                    <a href="https://www.instagram.com/zuehlkegroup/?hl=en" target="_blank"><FontAwesomeIcon icon={['fab', 'instagram']} /></a>
                </div>
                <div className="col">
                    <a href="https://twitter.com/zuehlke_group" target="_blank"><FontAwesomeIcon icon={['fab', 'twitter-square']} /></a>
                    <a href="https://www.youtube.com/channel/UCDglr0_rdf7cIakhluxAeBA" target="_blank"><FontAwesomeIcon icon={['fab', 'youtube']} /></a>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Footer;
