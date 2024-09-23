import React, { useState, useEffect } from "react";
import PropTypes from 'prop-types';

import styles from './Home.module.css';
import Header from '../../_layouts/Headers/Headers';
import Sidebar from '../../_layouts/Sidebar/Sidebar';
import Footer from '../../_layouts/Footers/Footers';
import Moment from 'moment';

const Home = () => {
  Moment.locale('en');
  const [user, setUser] = useState({ email: '', id: '' });

  useEffect(() => {
    // Retrieve user data from localStorage
    const savedUser = JSON.parse(localStorage.getItem('userDetails'));
    if (savedUser) {
      setUser(savedUser);
    }
  }, []);

  return (
    <div className={styles.Home} data-testid="Home">
      <Header title="Dashboard"></Header>
      <Sidebar></Sidebar>

      <div className="content-body">
		
        <div className="container-fluid">
		<div className="user-info mt-4">
            <h3>Welcome, {user.email}</h3>
            {/* <p>User ID: {user.id}</p> */}
          </div>
          <div className="row">
            <div className="col-xl-3 col-xxl-4">
              <div className="row">
                <div className="col-xl-12 col-md-6">
                  <div className="card">
                    <div className="card-body">
                      <div className="d-flex justify-content-between align-items-center">
                        <div>
                          <p className="fs-14 mb-1">Products </p>
                          <span className="fs-35 text-black font-w600">2359
                            <svg className="ml-1" width="19" height="12" viewBox="0 0 19 12"
                              fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path
                                d="M2.00401 11.1924C0.222201 11.1924 -0.670134 9.0381 0.589795 7.77817L7.78218 0.585786C8.56323 -0.195262 9.82956 -0.195262 10.6106 0.585786L17.803 7.77817C19.0629 9.0381 18.1706 11.1924 16.3888 11.1924H2.00401Z"
                                fill="#33C25B" />
                            </svg>
                          </span>
                        </div>
                        <div className="d-inline-block ml-auto position-relative donut-chart-sale">
                          <small className="text-secondary">90%</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="col-xl-12 col-md-6">
                  <div className="card">
                    <div className="card-header border-0 pb-0">
                      <h4 className="fs-20">McCoy</h4>
                      <select className="form-control style-1 default-select ">
                        <option>This Week</option>
                      </select>
                    </div>
                  
                    <div className="card-footer text-center border-0">
                      <a className="btn btn-primary btn-sm dz-load-more" id="latestSales"
                        href="http://127.0.0.1:3000/search" rel="ajax/latest-sales.html">View More</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-xl-9 col-xxl-8">
              <div className="row">
                <div className="col-xl-4 col-xxl-6 col-lg-4 col-sm-6">
                  <div className="card">
                    <div className="card-body">
                      <div className="d-flex align-items-end">
                        <div>
                          <p className="fs-14 mb-1">Search</p>
                          <span className="fs-35 text-black font-w600">23
                            <svg className="ml-1" width="19" height="12" viewBox="0 0 19 12"
                              fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path
                                d="M2.00401 11.1924C0.222201 11.1924 -0.670134 9.0381 0.589795 7.77817L7.78218 0.585786C8.56323 -0.195262 9.82956 -0.195262 10.6106 0.585786L17.803 7.77817C19.0629 9.0381 18.1706 11.1924 16.3888 11.1924H2.00401Z"
                                fill="#33C25B" />
                            </svg>
                          </span>
                        </div>
                        <div className="d-inline-block ml-auto position-relative donut-chart-sale">
                          <small className="text-secondary">70%</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="col-xl-4 col-xxl-6 col-lg-4 col-sm-6">
                  <div className="card">
                    <div className="card-body">
                      <div className="d-flex align-items-end">
                        <div>
                          <p className="fs-14 mb-1">Change</p>
                          <span className="fs-35 text-black font-w600">52
                            <svg className="ml-1" width="19" height="12" viewBox="0 0 19 12"
                              fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path
                                d="M2.00401 11.1924C0.222201 11.1924 -0.670134 9.0381 0.589795 7.77817L7.78218 0.585786C8.56323 -0.195262 9.82956 -0.195262 10.6106 0.585786L17.803 7.77817C19.0629 9.0381 18.1706 11.1924 16.3888 11.1924H2.00401Z"
                                fill="#33C25B" />
                            </svg>
                          </span>
                        </div>
                        <div className="d-inline-block ml-auto position-relative donut-chart-sale">
                          <small className="text-secondary">90%</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Display User Information */}
       
        </div>
        
      </div>
	  <Footer></Footer>
    </div>
  );
}

Home.propTypes = {
  title: PropTypes.string,
};

export default Home;
