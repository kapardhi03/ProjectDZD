import React, { useState } from "react";
import "./Register.css";
import { useHistory, Link } from "react-router-dom";
import Navbar from "./Navbar";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();
  const [error, setError] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Send registration request to the backend
    fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      body: JSON.stringify({ username: username, password: password }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message === "User registered successfully") {
          // Store login details in local storage
          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("username", username);

          // Redirect to the home page
          history.push("/");
        } else if (data.message === "Username already exists") {
          setError("Username already exists. Please try a different username.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    // Clear form inputs
    setUsername("");
    setPassword("");
  };

  return (
    <div className="registerbody">
      <Navbar />
      <div className="register-container">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="email"
              id="username"
              value={username}
              onChange={handleUsernameChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={handlePasswordChange}
            />
          </div>
          <button type="submit">Register</button>
          <p>
            Already have an account? <Link to="/login">Login</Link>
          </p>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Register;
