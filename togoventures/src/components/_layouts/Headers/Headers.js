import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";
import styles from './Headers.module.css';


function Header(props) {
  const { title, subtitle } = props; 
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState([]);
  const [results, setResults] = useState([]);
  const [loggedIn, setLoggedIn] = useState(false);
  const [items, setItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    let gotten = JSON.parse(localStorage.getItem("gunduauser"));
    if (!gotten && window.location.pathname !== "/login") {
      setResults([]);
      return;
    } else {
      let token = gotten?.data?.refresh;
      let payload = { "refresh": token };
      setTimeout(() => logOut(), 3600000);
    }
  }, []);

  const logOut = () => {
    localStorage.removeItem('gunduauser');
    navigate('/login');
  };

  return (
    <div>
      {/* Nav header start */}
      <div className="nav-header">
        <a href="/" className="brand-logo">
          {/* Logo goes here */}
        </a>
        <div className="nav-control">
          <div className="hamburger">
            <span className="line"></span>
            <span className="line"></span>
            <span className="line"></span>
          </div>
        </div>
      </div>
      {/* Nav header end */}

      {/* Header start */}
      <div className="header">
        <div className="header-content">
          <nav className="navbar navbar-expand">
            <div className="collapse navbar-collapse justify-content-between">
              <div className="header-left">
                <div className="dashboard_bar">
                  {title}
                  <span className={styles.subtitle}>{subtitle}</span> {/* Displaying the subtitle */}
                </div>
              </div>
            
              <ul className="navbar-nav header-right">

                  {/* Button added here */}

                  <li className="nav-item">
                    <button className={`btn btn-primary ${styles.customButton}`} onClick={() => navigate('/Search2')}>
                      Request Estimate
                    </button>
                </li>

                <li className="nav-item dropdown header-profile">
                  <a className="nav-link" href="javascript:void(0)" role="button" data-toggle="dropdown">
                    <img src="./images/profile/rename.png" width="20" alt="profile" />
                  </a>
                  <div className="dropdown-menu dropdown-menu-right">
                    <a href="/profile" className="dropdown-item ai-icon">
                      <span className="ml-2">Profile</span>
                    </a>
                    <a href="javascript:void(0);" onClick={logOut} className="dropdown-item ai-icon">
                      <span className="ml-2">Logout</span>
                    </a>
                  </div>
                </li>

              
              
              </ul>
            </div>
          </nav>
        </div>
      </div>
      {/* Header end */}
    </div>
  );
}

Header.propTypes = {
  title: PropTypes.string,   // Existing prop
  subtitle: PropTypes.string // New subtitle prop
};

Header.defaultProps = {
  title: 'Login',
  subtitle: ''               // Default empty subtitle
};

export default Header;
