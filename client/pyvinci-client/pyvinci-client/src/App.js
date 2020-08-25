import React, {useState, useEffect} from 'react'
import './App.css';
import { Home } from './ui/views/Home/Home';
import { Project } from './ui/views/Project/Project';
import { CreateProject } from './ui/views/CreateProject/CreateProject';
import { Register } from './ui/views/Register/Register';
import { Login } from './ui/views/Login/Login';
import Nav from './ui/components/Nav/Nav.js';
import Axios from "axios";
import UserService from './services/UserService';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

Axios.interceptors.request.use(
  req => {
    // Set Authorization header, if token exists
    const token = UserService.getToken()
    if(token){
      req.headers.authorization = `Bearer ${token}`
    }
    return req;
  },
  error => {
    return Promise.reject(error);
  }
);

function App() {
     
  const [isLoggedIn, setIsLoggedIn] = useState(UserService.isLoggedIn());
  useEffect(() => {
    const listener = (newIsLogged) => {
      setIsLoggedIn(newIsLogged)
    };
    UserService.subscribe(listener)
    return () => {
      UserService.unsubscribe(listener)
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <Nav isLoggedIn={isLoggedIn}/>
        <Switch>

          <Route exact path="/login" component={Login} />
          <Route exact path="/register" component={Register} />

          {!isLoggedIn ? <Redirect to='/login' /> : null}

          <Route path="/home" component={Home} />
          <Route path="/projects/new" component={CreateProject} />
          <Route path="/projects/:id" component={Project} />

        </Switch>
        
      </div>
    </Router>
  );
}

export default App;
