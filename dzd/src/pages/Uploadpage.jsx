import React from 'react'
import "./Upload.css";
import Navbar from './Navbar';
const Uploadpage = () => {
    return (
        <div>
            <Navbar/>
            <div className="bottom-container">
                <div className="Link">
                    <a className="footer-link" href="https://www.linkedin.com/">@LinkedIn</a>
                    <span className="link-space"></span>
                    <a className="footer-link" href="https://twitter.com/">@Twitter</a>
                    <span className="link-space"></span>
                    <a className="footer-link" href="https://www.instagram.com/kapardhi.kannekanti/">@Instagram</a>
                </div>
                <p className="cpyryt">©detectiveZeroDay.</p>
                
            </div>
        </div>
    )
}

export default Uploadpage