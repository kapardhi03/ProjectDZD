import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import "./Nav.css";

const Navbar = () => {
  const [navbarVisible, setNavbarVisible] = useState(true);

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.pageYOffset;
      const showNavbar = scrollPosition === 0;
      setNavbarVisible(showNavbar);
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <section id='nav'>
      <nav className={`navbar navbar-expand-lg navbar-dark bg-dark fixed-top ${navbarVisible ? '' : 'navbar-hidden'}`}>
        <div className="container-fluid">
          <a className="navbar-brand" href="#">DZD</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarContent">
            <ul className="navbar-nav ms-auto me-3">
              <li className='nav-item'>
                <a className='nav-link active' aria-current="page" href='/AboutUs'>About</a>
              </li>
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="/">Home</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </section>
  );
}

export default Navbar;
