import React from 'react';
import ReactDOM from 'react-dom'
import './index.css';
// import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Pages/Home/Home';
import Login from './components/Login/Login';
// import Profile from './components/Profile/Profile';
import Profile from './Profile/Profile';
import Register from './components/Register/Register';
import Products from './components/Pages/products/Products';
import Search from './components/Pages/products/Search';
import Search2 from './components/Pages/products/Search2';
ReactDOM.render(
  <BrowserRouter>
    <Routes>
      <Route exact path="/register" element={<Register />} />
      <Route exact path="/login" element={<Login />} />
      <Route exact path="/profile" element={<Profile />} />
    
      <Route exact path="/" element={<Home />} />
      <Route path="/Search" element={<Search />} />
      <Route path="/Search2" element={<Search2 />} />
      <Route exact path="/products" element={<Products />} />


  
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);



reportWebVitals();
