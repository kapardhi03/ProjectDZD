import React from 'react';
import { useHistory } from 'react-router-dom';
import Navbar from './Frontpage';
import "./home_styles.css";
import Upload from './Upload';

const Home = () => {
  const history = useHistory();

  const handleTryNow = () => {
    
    const isAuthenticated = localStorage.getItem("isLoggedIn") === "true";

    if (isAuthenticated) {
      history.push('/Upload'); 
    } else {
      history.push('/login'); 
    }
  };

  return (
    <div>
      <Navbar />
      <button className='uploadButton' onClick={handleTryNow}>Try it now</button>
    </div>
  );
};

export default Home;
