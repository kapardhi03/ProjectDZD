import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import Upload from './pages/Upload';
// import FrontPage from './FrontPage';

function FrontPage() {
  const [showUploadPage, setShowUploadPage] = useState(false);

  const handleScheduleDemoClick = () => {
    setShowUploadPage(true);
  };

  return (
    <div>
        {/* <p>Hello</p> */}
    </div>
  );
}

export default FrontPage;
