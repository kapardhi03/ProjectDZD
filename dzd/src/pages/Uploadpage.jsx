import React from 'react'
import "./Upload.css";
import Navbar from './Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLinkedin, faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';

const Uploadpage = () => {
    return (
        <div>
            <Navbar/>
            <div className="bottom-container">
                <div className="Link">
                <FontAwesomeIcon icon={faLinkedin} />
                    <a className="footer-link" href="https://www.linkedin.com/in/kapardhi-kannekanti-a91a4325b/">LinkedIn</a>
                    
                    <span className="link-space"></span>
                    <FontAwesomeIcon icon={faTwitter} />
                    <a className="footer-link" href="https://twitter.com/kapardhi200903">Twitter</a>
                    <span className="link-space"></span>
                    <FontAwesomeIcon icon={faInstagram} />
                    <a className="footer-link" href="https://www.instagram.com/kapardhi.kannekanti/">Instagram</a>
                </div>
                <p className="cpyryt">© 2023-DetectivedZeroDay. All rights reserved.</p>
                
            </div>
        </div>
    )
}

export default Uploadpage