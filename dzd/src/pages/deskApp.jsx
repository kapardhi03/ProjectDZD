import React, { Component } from 'react';
import './deskApp.css';

export class DeskApp extends Component {
  render() {
    return (
      <div className="desk-app">
        <h1 className="title">Welcome!</h1>
        <p className="description">Click here, and we'll take care of everything for you.</p>
        <button className="cta-button">Get Started</button>
      </div>
    );
  }
}

export default DeskApp;
