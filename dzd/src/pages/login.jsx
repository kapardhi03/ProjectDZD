import React, { useState, useEffect } from "react";
import "./Login.css";
import { useHistory, Link } from "react-router-dom";
import Navbar from "./Navbar";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const history = useHistory();

  useEffect(() => {
    setError("");
  }, []);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
    setError(""); // Reset error when username changes
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
    setError(""); // Reset error when password changes
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Send login request to the backend
    const endpoint = "/login";
    const requestData = {
      username: username,
      password: password,
    };

    fetch("\https://hackers-nn94.onrender.com/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Login request failed.");
        }
        return response.json();
      })
      .then((data) => {
        if (data.message === "Login successful") {
          // Store login details in local storage
          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("username", username);
          history.push("/");
          // Call onLogin function to update login status in App.js
          onLogin();

          // Reset error state
          setError("");

          // Redirect to the home page
          
        } else {
          setError("Invalid credentials");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        // setError("Login request failed. Please try again.");
      });

    // Clear form inputs
    setUsername("");
    setPassword("");
  };

  return (
    <div className="login-container">
      <Navbar />
      <div className="login-box">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={handleUsernameChange}
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={handlePasswordChange}
            />
          </div>
          <button type="submit">Login</button>
        </form>
        {error && <p className="error-message">{error}</p>}
        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
