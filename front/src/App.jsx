import { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";
import Home from "./pages/Home/Home";
import Signup from "./pages/Signup/Signup";
import Signin from "./pages/Signin/Signin";

function App() {
  return (
    <Router>
    <Routes>
        <Route path={'/'} element={<Home/>} />
        <Route path={'/library'} element={<Home/>} />
        <Route path={'/sign-up'} element={<Signup/>} />
        <Route path={'/sign-in'} element={<Signin/>} />
    </Routes>
  </Router>
  );
}

export default App;
