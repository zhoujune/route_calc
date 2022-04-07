import React, { Component } from "react";
import ReactDOM from 'react-dom';
import {render} from 'react-dom';
import PaymentForm from "./Main";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect,
  } from "react-router-dom";
  

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
          <PaymentForm></PaymentForm>
        <Router>
          <Routes>
            
          </Routes>
        </Router>
      </div>
    );
  }
}

const appDiv = document.getElementById("app")
render(<App />, appDiv);
