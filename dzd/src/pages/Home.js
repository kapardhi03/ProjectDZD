import React from 'react';
// import Navbar from './Navbar';
import Navbar from './Frontpage';
import FrontPage from '../FrontPage';
import "./home_styles.css"
// import instructions from './instructions';
const Home = () => {
  return (
    <div>
        <Navbar/>
      
      <a  href="/Upload">
        <button   class='uploadButton'>Try it now</button>
      </a>
      <a href='instructions'>
        
      </a>
    </div>
  );
};

export default Home;
