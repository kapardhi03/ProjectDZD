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
