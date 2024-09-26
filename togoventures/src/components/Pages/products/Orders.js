import React, { useState, useEffect } from "react";
import PropTypes from 'prop-types';

import styles from './Home.module.css';
import Header from '../../_layouts/Headers/Headers';
import Sidebar from '../../_layouts/Sidebar/Sidebar';
import Footer from '../../_layouts/Footers/Footers';
import Moment from 'moment';
import supabase from "../../../config/supabaseClient";

const Order = () => {
  const [userId, setUserId] = useState('');
  const [media, setMedia] = useState([]);
  const [user, setUser] = useState({ email: '', id: '' });

  Moment.locale('en');

  // UseEffect to get user data from localStorage
  useEffect(() => {
    const savedUser = JSON.parse(localStorage.getItem('userDetails'));
    if (savedUser) {
      setUser(savedUser);
      setUserId(savedUser.id); // Set userId when user is retrieved
    }
  }, []);

  // Fetch media from Supabase Storage
  const getMedia = async () => {
    if (!userId) return; // Ensure userId is set before fetching media

    const { data, error } = await supabase.storage.from("test").list(userId + "/", {
      limit: 10,
      offset: 0,
      sortBy: { column: "name", order: "asc" },
    });

    if (data) {
      setMedia(data);
    } else {
      console.error("Error fetching media:", error);
    }
  };

  // Call getMedia whenever userId changes
  useEffect(() => {
    getMedia();
  }, [userId]);

  return (
    <div className={styles.Home} data-testid="Home">
      <Header title="Dashboard"></Header>
      <Sidebar></Sidebar>

      <div className="content-body">
        <div className="container-fluid">
          <div className="user-info mt-4">
            <h3>Welcome, {user.email}</h3>
            <p>User ID: {user.id}</p>
          </div>
          <div className="row">
  {media.length > 0 ? media.map((item, index) => (
    <div className="col-xl-4 col-xxl-6 col-lg-4 col-sm-6" key={item.name}>
      <div className="card mb-4"> {/* Added margin-bottom for spacing between cards */}
        <div className="card-body">
          <div className="d-flex flex-column align-items-center">
            {/* <img 
              src={`https://ovlhvogwndcqxaskukrv.supabase.co/storage/v1/object/public/uploads/${userId}/${item.name}`} 
              alt={item.name} // Use item.name for alt text for better accessibility
              style={{ maxWidth: '100%', height: 'auto', borderRadius: '5px' }} // Added border-radius for styling
            /> */}
            <p className="mt-2">{item.name}</p> {/* Displaying the actual file name */}
          </div>
        </div>
      </div>
    </div>
  )) : (
    <p>No media available</p>
  )}
</div>

        </div>
      </div>
      <Footer></Footer>
    </div>
  );
}

Order.propTypes = {
  title: PropTypes.string,
};

export default Order;
