
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import AboutUs from "./pages/AboutUs";

import Instructions from "./pages/instructions";

const App = () => {
  const [isLoggedIn, setLoggedIn] = useState(localStorage.getItem("isLoggedIn") === "true");

  const handleLogin = () => {
    setLoggedIn(true);
  };

  const handleRegister = () => {
    setLoggedIn(true);
  };
  if (isLoggedIn){
    return (
      <Router>
        <Switch>
  
        <Route path="/register" component={Register} />
        <Route path="/login" component = {Login}/>
        <Route exact path="/" component={Home}/>
        <Route path="/AboutUs" component={AboutUs}/>
        <Route path="/Upload" component={Upload}/>
        <Route path="/instructions" component={Instructions}/>
          <Route exact path="/">
            {isLoggedIn ? (
              <Home />
            ) : (
              <Redirect to="/login" />
            )}
          </Route>
          <Route path="/login">
            {isLoggedIn ? (
              <Redirect to="/" />
            ) : (
              <Login onLogin={handleLogin} />
            )}
          </Route>
          <Route path="/register">
            {isLoggedIn ? (
              <Redirect to="/" />
            ) : (
              <Register onRegister={handleRegister} />
            )}
          </Route>
          <Route path="/Upload">
            {isLoggedIn ? (
              <Redirect to="/Upload" />
            ) : (
              <Redirect to="/login" />
            )}
          </Route>
        </Switch>
      </Router>
    );
  }
  else{

  
  return (
    <Router>
      <Switch>

      <Route path="/register" component={Register} />
      <Route path="/login" component = {Login}/>
      <Route exact path="/" component={Home}/>
      <Route path="/AboutUs" component={AboutUs}/>
     
        <Route exact path="/">
          {isLoggedIn ? (
            <Home />
          ) : (
            <Redirect to="/login" />
          )}
        </Route>
        <Route path="/login">
          {isLoggedIn ? (
            <Redirect to="/" />
          ) : (
            <Login onLogin={handleLogin} />
          )}
        </Route>
        <Route path="/register">
          {isLoggedIn ? (
            <Redirect to="/" />
          ) : (
            <Register onRegister={handleRegister} />
          )}
        </Route>
        <Route path="/Upload">
          {isLoggedIn ? (
            <Redirect to="/Upload" />
          ) : (
            <Redirect to="/login" />
          )}
        </Route>
      </Switch>
    </Router>
  );
          }
};

export default App;
