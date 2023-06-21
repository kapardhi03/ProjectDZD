<<<<<<< HEAD
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Upload from './pages/Upload';
import FrontPage from './FrontPage';
import instructions from './pages/instructions';

function App() {
  

  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Home} />    
        <Route path="/Upload" component={Upload} />
        <Route path =  '/FrontPage' component = {FrontPage}/>
        <Route path = '/instructions' component = {instructions}/>
      </Switch>
    </Router>
  );
}

export default App;
=======
import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [res, setres] = useState("");

  const handleChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        mode: 'no-cors'
      });
      setres(response.data);
      console.log(res);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>

    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleChange} />
      <button type="submit">Check</button>
      {res && (
      <div>
        <p>Result: {res.Prediction}</p>
        <p>Non - malicious Samples: {res.nonmal}</p>
        <p>Malicious Samples: {res.mali}</p>
        <p>Type of the attack: {res.attack}</p>
        <p>More information:{res.info}</p>
      </div>
    )}
    </form>
    </div>
  );
}

export default FileUpload;
>>>>>>> 29b4dd63a314a90a91a8cb84542fd0e7307dc748
